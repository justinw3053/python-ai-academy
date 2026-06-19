// app.js

let editor;
let worker;
let inputBuffer;
let inputView;

let lessons = [];
let currentLessonIndex = 0;
let currentExerciseIndex = 0;

// Initialize Monaco Editor and Load Lessons
window.addEventListener('DOMContentLoaded', () => {
    // 1. Set up AMD Loader configuration
    const script = document.createElement('script');
    script.src = './vs/loader.js';
    script.onload = () => {
        require.config({ paths: { 'vs': './vs' } });
        require(['vs/editor/editor.main'], function () {
            editor = monaco.editor.create(document.getElementById('monaco-container'), {
                value: '# Loading curriculum...',
                language: 'python',
                theme: 'vs-dark',
                automaticLayout: true,
                fontSize: 14,
                minimap: { enabled: false }
            });
            // After Monaco is loaded, load lessons list
            loadLessonsList();
        });
    };
    document.body.appendChild(script);

    // 2. Initialize Web Worker
    initWorker();

    // 3. Set up run button
    document.getElementById('run-btn').addEventListener('click', runCode);

    // 4. Set up Pi Agent Chat
    document.getElementById('chat-send').addEventListener('click', sendChatMessage);
    document.getElementById('chat-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendChatMessage();
    });
});

function initWorker() {
    // Setup SharedArrayBuffer for synchronous input
    if (window.SharedArrayBuffer) {
        inputBuffer = new SharedArrayBuffer(1024);
        inputView = new Int32Array(inputBuffer);
    } else {
        console.warn("SharedArrayBuffer is not supported. Synchronous input() will not function.");
    }

    worker = new Worker('worker.js');

    if (inputBuffer) {
        worker.postMessage({ type: 'init_buffer', buffer: inputBuffer });
    }

    worker.onmessage = (event) => {
        let data = event.data;
        if (typeof data === 'string') {
            try {
                data = JSON.parse(data);
            } catch (e) {}
        }
        if (data.type === 'stdout') {
            printToTerminal(data.message);
        } else if (data.type === 'execution_success') {
            printToTerminal('\n[SUCCESS] Εκτέλεση επιτυχής!\n', 'success');
            // Save progress to state manager on backend
            saveLessonProgress();
        } else if (data.type === 'execution_error') {
            printToTerminal(`\n[ERROR] ${data.error}\n`, 'error');
        } else if (data.type === 'input_request') {
            handleInputRequest(data.prompt);
        }
    };
}

function handleInputRequest(promptText) {
    if (!inputView) return;
    const userInput = prompt(promptText || "Python input:") || "";
    printToTerminal(userInput + '\n');

    const encoder = new TextEncoder();
    const stringBytes = encoder.encode(userInput);
    const length = stringBytes.length;

    inputView[1] = length;
    const bufferBytes = new Uint8Array(inputBuffer, 8);
    bufferBytes.set(stringBytes);

    Atomics.store(inputView, 0, 1);
    Atomics.notify(inputView, 0);
}

function printToTerminal(message, type = '') {
    const term = document.getElementById('output-content');
    if (type === 'success') {
        term.innerHTML += `<span style="color: var(--success-color);">${message}</span>`;
    } else if (type === 'error') {
        term.innerHTML += `<span style="color: var(--error-color);">${message}</span>`;
    } else {
        term.innerHTML += message;
    }
    // Auto scroll to bottom
    const container = document.getElementById('terminal-output');
    container.scrollTop = container.scrollHeight;
}

// Lessons Engine
async function loadLessonsList() {
    try {
        const response = await fetch('/api/lessons');
        lessons = await response.json();
        
        if (lessons.length > 0) {
            // Find current lesson from local progress or start with first Greek lesson
            currentLessonIndex = 0;
            loadLesson(lessons[currentLessonIndex].id);
        } else {
            document.getElementById('narrative-content').innerHTML = `
                <h1>Σφάλμα</h1>
                <p>Δεν βρέθηκαν μαθήματα στο φάκελο content.</p>
            `;
        }
    } catch (e) {
        console.error(e);
        document.getElementById('narrative-content').innerHTML = `
            <h1>Σφάλμα</h1>
            <p>Αποτυχία φόρτωσης μαθημάτων από το backend.</p>
        `;
    }
}

async function loadLesson(lessonId) {
    try {
        document.getElementById('narrative-content').innerHTML = `<h1>Φόρτωση μαθήματος...</h1>`;
        const response = await fetch(`/api/lessons/${lessonId}`);
        const data = await response.json();

        // Render Narrative
        document.getElementById('narrative-content').innerHTML = formatMarkdown(data.markdown);
        
        // Add navigation button to next lesson if any
        if (currentLessonIndex < lessons.length - 1) {
            const nextBtn = document.createElement('button');
            nextBtn.style.marginTop = '20px';
            nextBtn.innerText = 'ΕΠΟΜΕΝΟ ΜΑΘΗΜΑ (NEXT)';
            nextBtn.onclick = () => {
                currentLessonIndex++;
                currentExerciseIndex = 0;
                loadLesson(lessons[currentLessonIndex].id);
            };
            document.getElementById('narrative-content').appendChild(nextBtn);
        }

        // Initialize editor with first exercise starter code
        currentExerciseIndex = 0;
        if (data.exercises && data.exercises.length > 0) {
            editor.setValue(data.exercises[currentExerciseIndex].starter_code);
        } else {
            editor.setValue('# Start coding...');
        }
        
        document.getElementById('output-content').innerText = '>';
    } catch (e) {
        console.error(e);
        document.getElementById('narrative-content').innerHTML = `<h1>Σφάλμα</h1><p>Αποτυχία φόρτωσης λεπτομερειών μαθήματος.</p>`;
    }
}

function runCode() {
    if (!editor || !worker) return;
    const code = editor.getValue();
    
    document.getElementById('output-content').innerText = '>';
    printToTerminal('Εκτέλεση κώδικα...\n');

    // Get current exercise hidden assertions
    let assertions = "";
    let required_ast = [];
    
    fetch(`/api/lessons/${lessons[currentLessonIndex].id}`)
        .then(res => res.json())
        .then(lessonData => {
            const exercise = lessonData.exercises && lessonData.exercises[currentExerciseIndex];
            if (exercise) {
                assertions = exercise.assertions || "";
            }
            
            // Append assertions to the run code so that they are executed together in the worker
            const fullCode = code + (assertions ? "\n\n" + assertions : "");
            
            // Extract required AST nodes (e.g. if instruction mentions loop, check for 'For' or 'While')
            const reqAst = [];
            if (lessonData.markdown.toLowerCase().includes('για (for)') || lessonData.markdown.toLowerCase().includes('for loop')) {
                reqAst.push('For');
            }
            if (lessonData.markdown.toLowerCase().includes('while loop') || lessonData.markdown.toLowerCase().includes('while')) {
                reqAst.push('While');
            }
            
            worker.postMessage({
                type: 'run_code',
                code: fullCode,
                required_ast: reqAst
            });
        });
}

async function saveLessonProgress() {
    const currentLesson = lessons[currentLessonIndex];
    if (!currentLesson) return;
    try {
        await fetch('/api/track', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ lesson: currentLesson.id })
        });
    } catch (e) {
        console.error("Failed to save progress:", e);
    }
}

// Socratic Pi Agent Chat
async function sendChatMessage() {
    const inputEl = document.getElementById('chat-input');
    const message = inputEl.value.trim();
    if (!message) return;

    inputEl.value = '';
    appendChatMessage('Leonidas', message);

    // Get current code for context
    const currentCode = editor ? editor.getValue() : '';
    const currentLesson = lessons[currentLessonIndex];
    const lessonId = currentLesson ? currentLesson.id : '';

    const chatHistory = document.getElementById('chat-history');
    const aiBubble = appendChatMessage('Pi Agent', '...');
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                context: currentCode,
                lessonId: lessonId
            })
        });

        if (!response.ok) {
            aiBubble.innerText = 'Error communicating with AI.';
            return;
        }

        // Handle streaming via Server-Sent Events (SSE)
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let aiText = '';
        aiBubble.innerText = '';
        let buffer = '';

        function processSSELine(line) {
            if (line.startsWith('data: ')) {
                const dataStr = line.slice(6).replace(/\r$/, '');
                if (dataStr.trim() === '[DONE]') return;
                
                // The backend streams raw content with \n replaced by \\n
                const content = dataStr.replace(/\\n/g, '\n');
                aiText += content;
                aiBubble.innerHTML = formatMarkdown(aiText);
                chatHistory.scrollTop = chatHistory.scrollHeight;
            }
        }

        while (true) {
            const { done, value } = await reader.read();
            if (done) {
                if (buffer) {
                    processSSELine(buffer);
                }
                break;
            }

            const chunk = decoder.decode(value, { stream: true });
            buffer += chunk;
            
            const lines = buffer.split('\n');
            // Hold back the last incomplete line
            buffer = lines.pop();
            
            for (const line of lines) {
                processSSELine(line);
            }
        }
    } catch (e) {
        console.error(e);
        aiBubble.innerText = 'Error connecting to mentor system.';
    }
}

function appendChatMessage(sender, text) {
    const chatHistory = document.getElementById('chat-history');
    const wrapper = document.createElement('div');
    wrapper.style.marginBottom = '12px';
    wrapper.style.clear = 'both';
    wrapper.style.width = '100%';
    wrapper.style.display = 'flow-root';
    
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${sender === 'Leonidas' ? 'student-bubble' : 'agent-bubble'}`;
    
    const senderEl = document.createElement('strong');
    senderEl.innerText = `${sender}: `;
    senderEl.style.display = 'block';
    senderEl.style.marginBottom = '4px';
    senderEl.style.fontSize = '0.85em';
    senderEl.style.color = sender === 'Leonidas' ? '#1b4d8a' : '#b27500';
    
    const textEl = document.createElement('span');
    textEl.innerHTML = formatMarkdown(text);
    
    bubble.appendChild(senderEl);
    bubble.appendChild(textEl);
    wrapper.appendChild(bubble);
    chatHistory.appendChild(wrapper);
    
    chatHistory.scrollTop = chatHistory.scrollHeight;
    return textEl;
}

// Simple Markdown parser
function formatMarkdown(text) {
    if (!text) return '';
    // Replace markdown headers, bold, code, and list items
    let html = text
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/gim, '<em>$1</em>')
        .replace(/`(.*?)`/gim, '<code>$1</code>')
        .replace(/\n/g, '<br/>');
    return html;
}
