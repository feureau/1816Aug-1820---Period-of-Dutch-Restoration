/**
 * Dynamic Markdown Loader for Dutch Restoration Documentation
 * Uses FileReader API to work with file:// protocol (no CORS issues)
 */

const containerId = 'markdown-content';

// Initialize page structure first
document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById(containerId);
    
    // Create placeholder until file loads
    container.style.display = 'none';
    container.innerHTML = `
        <div style="background-color: #2d2d2d; padding: 30px; border-radius: 5px; border-left: 4px solid #4a9eff;">
            <h3 style="color: #4a9eff; margin-top: 0;">Dutch Restoration Documentation (1816–1820)</h3>
            <p>Loading historical content from Markdown source...</p>
            <div style="background-color: #2d2d2d; padding: 15px; border-radius: 4px; border-left: 3px solid #ff6b6b;">
                <p><strong>Please note:</strong> You must open this page using a web server (e.g., Python `python -m http.server`) rather than double-clicking the file.</p>
                <p style="margin-top: 10px;">This is a browser security requirement - local files cannot be fetched via JavaScript from the file:// protocol.</p>
                <p style="margin-top: 10px;"><strong>Quick Fix:</strong> Open Command Prompt and run:<br><code>cd "F:\\GitHub\\1816Aug-1820 - Period of Dutch Restoration"</code><br>then navigate to this page at:</p>
                <code style="background-color: #1a1a1a; color: #4a9eff; padding: 5px 10px;">http://localhost:8000/</code>
            </div>
        </div>
    `;
    
    // Try to load markdown file if accessible (works in some browsers with http server)
    tryLoadMarkdownFile();
});

// Fallback: Read file using FileReader for local file:// access
function tryReadLocalFile() {
    const container = document.getElementById(containerId);
    
    // Create input element for file reading
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.md';
    input.style.display = 'none';
    
    document.body.appendChild(input);
    input.onchange = function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                renderMarkdown(event.target.result);
            };
            reader.onerror = function() {
                showError(container, 'Could not read the markdown file');
            };
            
            // Read entire file as text
            if (file.size < 2000000) { // Max 2MB
                reader.readAsText(file);
            } else {
                showError(container, 'File is too large (' + formatFileSize(file.size) + ')');
            }
        }
    };
    
    // Trigger file picker
    input.click();
}

// Try fetch first (works with http server), fallback to FileReader
async function tryLoadMarkdownFile() {
    const container = document.getElementById(containerId);
    const mdUrl = '1816Aug-1820 - Period of Dutch Restoration.md';
    
    try {
        // Try HTTP fetch first
        const response = await fetch(mdUrl);
        
        if (response.ok) {
            const markdown = await response.text();
            renderMarkdown(markdown);
            return;
        } else {
            throw new Error('HTTP fetch failed');
        }
    } catch (error) {
        console.log('File fetch not available (file:// protocol). Showing file picker.');
        // Fallback to FileReader for local files
        tryReadLocalFile();
    }
}

function renderMarkdown(markdownText) {
    const container = document.getElementById(containerId);
    
    try {
        const htmlContent = parseMarkdown(markdownText);
        container.innerHTML = htmlContent;
        container.style.display = 'block';
        
        // Scroll to content
        container.scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        console.error('Markdown parsing error:', error);
        showError(container, 'Error parsing markdown: ' + error.message);
    }
}

/**
 * Simple markdown parser supporting common features
 */
function parseMarkdown(md) {
    let html = '';
    const lines = md.split('\n');
    let i = 0;
    let currentPara = [];
    let inList = false;
    let blockquote = false;
    
    while (i < lines.length) {
        const line = lines[i];
        
        // Empty line ends paragraph
        if (line.trim() === '' && currentPara.length > 0) {
            html += flushParagraph();
            inList = false;
            blockquote = false;
            currentPara = [];
            i++;
            continue;
        }
        
        // Code blocks
        if (line.trim() === '```') {
            html += '<pre><code>';
            // Handle code content between backticks
            while (i + 1 < lines.length && !lines[i + 1].trim().startsWith('```')) {
                const codeLine = escapeHtmlCode(lines[i + 1]);
                if (!html.includes('</code>')) html += '<br>';
                html += codeLine;
                i++;
            }
            if (currentPara.length > 0) {
                currentPara = [];
                html += flushParagraph();
            }
            html += '</code></pre>';
            blockquote = false;
            i++;
            continue;
        }
        
        // Blockquotes
        if (line.trim().startsWith('>')) {
            if (!blockquote) {
                if (currentPara.length > 0) {
                    html += flushParagraph();
                    currentPara = [];
                }
                blockquote = true;
                html += '<blockquote>\n';
            }
            const bqText = escapeHtml(formatInline(line.substring(1).trim()));
            html += '<p>' + bqText + '</p>\n';
            i++;
            continue;
        } else if (blockquote) {
            html += '</blockquote>';
            blockquote = false;
        }
        
        // List items
        if (line.match(/^\s*- /)) {
            if (!inList) {
                html += flushParagraph();
                currentPara = [];
                inList = true;
            }
            const listItem = escapeHtml(formatInline(line.substring(2).trim()));
            html += '<li>' + listItem + '</li>\n';
        } else if (inList && line.trim() !== '') {
            // Close list
            html += '</ul>';
            inList = false;
            currentPara.push(formatInline(line));
        } else if (line.match(/^#{1,3}\s+/)) {
            // Headers
            if (currentPara.length > 0 && !inList && !blockquote) {
                html += flushParagraph();
            }
            
            const match = line.match(/^(#{1,3})\s+(.+)$/);
            if (match) {
                const hLevel = '#' + match[1].length;
                let tag = 'h' + match[1].length;
                html += '<' + tag + '>' + escapeHtml(formatInline(match[2])) + '</' + tag + '>\n';
            }
        } else if (line.trim() !== '') {
            // Regular paragraph text
            currentPara.push(formatInline(line));
        }
        
        i++;
    }
    
    // Close any open blocks
    if (inList) html += '</ul>';
    if (blockquote) html += '</blockquote>';
    
    // Final paragraph
    if (currentPara.length > 0) {
        html += flushParagraph();
    }
    
    return html;
}

function flushParagraph() {
    if (currentPara.length === 0) return '';
    
    let content = currentPara.join(' ');
    // Bold and italic
    content = content.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    content = content.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    // Links
    content = content.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" style="color: #4a9eff;">$1</a>');
    // Inline code (simple version)
    if (currentPara.length === 1 && currentPara[0].includes('`')) {
        content = '<code>' + currentPara[0] + '</code>';
    } else {
        content = content.replace(/`([^`]+)`/g, '`$1`');
    }
    
    return '<p>' + content + '</p>';
}

function formatInline(text) {
    // Process inline formatting for display
    text = escapeHtml(text);
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" style="color: #4a9eff;">$1</a>');
    return text;
}

function escapeHtml(text) {
    if (!text) return '';
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function escapeHtmlCode(text) {
    if (!text) return '';
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

function showError(container, message) {
    container.style.display = 'block';
    container.innerHTML = `
        <div style="background-color: #a63e3e; padding: 20px; border-radius: 5px; color: white;">
            <p><strong>Error:</strong> ${message}</p>
            <p style="margin-top: 15px;">To view the Dutch Restoration documentation properly, please run a local web server:</p>
            <div style="background-color: rgba(0,0,0,0.3); padding: 10px; border-radius: 4px; margin-top: 10px;">
                <p><strong>Method 1 (Recommended):</strong></p>
                <code style="color: #8ff;">python -m http.server 8000</code>
                <p style="margin-top: 5px;"><em>Then open:</em> <a href="http://localhost:8000/" style="color: #4fffff;">http://localhost:8000/</a></p>
            </div>
            <p style="margin-top: 10px;"><strong>Method 2:</strong> Use Node.js - run in folder:</p>
            <code style="background-color: rgba(0,0,0,0.3); padding: 5px 10px; border-radius: 4px;">npx http-server -p 8000</code>
        </div>
    `;
}

function formatFileSize(bytes) {
    const units = ['B', 'KB', 'MB', 'GB'];
    let unitIndex = 0;
    while (bytes >= 1024 && unitIndex < units.length - 1) {
        bytes /= 1024;
        unitIndex++;
    }
    return bytes.toFixed(1) + ' ' + units[unitIndex];
}
