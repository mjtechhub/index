/**
 * MJ Tech Hub - Commands Logic
 * Fetches commands from JSON and renders them with copy functionality.
 */

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('commands-container');
    if (!container) return;

    // Fetch commands data
    fetch('./data/commands.json')
        .then(response => {
            if (!response.ok) throw new Error('Failed to fetch commands');
            return response.json();
        })
        .then(commands => {
            renderCommands(commands, container);
        })
        .catch(error => {
            console.error('Error loading commands:', error);
            container.innerHTML = '<div class="card"><p style="color: var(--danger); text-align: center;">Failed to load commands. Please try again later.</p></div>';
        });

    function renderCommands(commands, container) {
        container.innerHTML = ''; // Clear loading
        
        commands.forEach((cmd, index) => {
            const card = document.createElement('div');
            card.className = 'card command-card';
            
            // Header
            const header = document.createElement('div');
            header.className = 'command-header';
            
            const title = document.createElement('h3');
            title.textContent = cmd.command;
            
            const platform = document.createElement('span');
            platform.className = 'command-platform';
            platform.textContent = cmd.platform;
            
            header.appendChild(title);
            header.appendChild(platform);
            card.appendChild(header);
            
            // Purpose
            const details = document.createElement('div');
            details.className = 'command-details';
            
            const purposeP = document.createElement('p');
            const purposeLabel = document.createElement('span');
            purposeLabel.className = 'command-label';
            purposeLabel.textContent = 'Purpose: ';
            purposeP.appendChild(purposeLabel);
            purposeP.appendChild(document.createTextNode(cmd.purpose));
            details.appendChild(purposeP);
            
            // Code block
            const codeBlock = document.createElement('div');
            codeBlock.className = 'command-code-block';
            
            const code = document.createElement('code');
            code.textContent = cmd.example;
            
            const copyBtn = document.createElement('button');
            copyBtn.className = 'copy-btn';
            copyBtn.innerHTML = '<i class="far fa-copy"></i> Copy';
            copyBtn.setAttribute('aria-label', `Copy ${cmd.command} to clipboard`);
            
            copyBtn.addEventListener('click', () => {
                navigator.clipboard.writeText(cmd.example).then(() => {
                    const originalHTML = copyBtn.innerHTML;
                    copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                    copyBtn.classList.add('copied');
                    
                    setTimeout(() => {
                        copyBtn.innerHTML = originalHTML;
                        copyBtn.classList.remove('copied');
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy text: ', err);
                });
            });
            
            codeBlock.appendChild(code);
            codeBlock.appendChild(copyBtn);
            details.appendChild(codeBlock);
            
            // Expected Result
            const resultP = document.createElement('p');
            const resultLabel = document.createElement('span');
            resultLabel.className = 'command-label';
            resultLabel.textContent = 'Expected Result: ';
            resultP.appendChild(resultLabel);
            resultP.appendChild(document.createTextNode(cmd.expectedResult));
            details.appendChild(resultP);
            
            // Use Case
            const useCaseP = document.createElement('p');
            const useCaseLabel = document.createElement('span');
            useCaseLabel.className = 'command-label';
            useCaseLabel.textContent = 'Use Case: ';
            useCaseP.appendChild(useCaseLabel);
            useCaseP.appendChild(document.createTextNode(cmd.useCase));
            details.appendChild(useCaseP);
            
            card.appendChild(details);
            
            // Warning if exists
            if (cmd.warnings) {
                const warningBox = document.createElement('div');
                warningBox.className = 'warning-box';
                warningBox.innerHTML = `<strong><i class="fas fa-exclamation-triangle"></i> Warning:</strong> ${cmd.warnings}`;
                card.appendChild(warningBox);
            }
            
            container.appendChild(card);
        });
    }
});
