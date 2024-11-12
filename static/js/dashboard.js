document.addEventListener('DOMContentLoaded', function() {
    // Navigation handling
    const navLinks = document.querySelectorAll('.nav-links a');
    const sections = document.querySelectorAll('.content-section');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const sectionName = link.dataset.section;
            
            // Update active link
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            // Show selected section
            sections.forEach(section => {
                section.classList.add('hidden');
                if (section.id === `${sectionName}-section`) {
                    section.classList.remove('hidden');
                }
            });
        });
    });

    // Fetch and display matches
    async function loadMatches() {
        try {
            const response = await fetch('/api/matches');
            const data = await response.json();
            const container = document.getElementById('matches-container');
            
            container.innerHTML = data.matches.map(match => `
                <div class="match-card">
                    <h3>${match.name}</h3>
                    <p>${match.age} years old</p>
                    <p>${match.match_percentage}% Match</p>
                    <button onclick="startChat(${match.id}, '${match.name}')" class="btn">Message</button>
                </div>
            `).join('');
            
            document.getElementById('matches-count').textContent = data.matches.length;
        } catch (error) {
            console.error('Error loading matches:', error);
        }
    }

    // Fetch and display messages
    async function loadMessages() {
        try {
            const response = await fetch('/api/messages');
            const data = await response.json();
            const container = document.getElementById('messages-container');
            
            container.innerHTML = data.messages.map(message => `
                <div class="message">
                    <strong>${message.from}</strong>
                    <p>${message.content}</p>
                    <small>${message.timestamp}</small>
                </div>
            `).join('');
            
            document.getElementById('messages-count').textContent = data.messages.length;
        } catch (error) {
            console.error('Error loading messages:', error);
        }
    }

    // Fetch and display runs
    async function loadRuns() {
        try {
            const response = await fetch('/api/runs');
            const data = await response.json();
            const container = document.getElementById('runs-container');
            
            container.innerHTML = data.runs.map(run => `
                <div class="run-card">
                    <div>
                        <strong>${run.date}</strong>
                        <p>Distance: ${run.distance}</p>
                    </div>
                    <div>
                        <p>Time: ${run.time}</p>
                    </div>
                </div>
            `).join('');
            
            document.getElementById('runs-count').textContent = data.runs.length;
        } catch (error) {
            console.error('Error loading runs:', error);
        }
    }

    // Initialize dashboard
    loadMatches();
    loadMessages();
    loadRuns();
});

// Chat functionality
let currentChatMatch = null;

function startChat(matchId, matchName) {
    currentChatMatch = matchId;
    
    // Show chat interface and hide messages list
    document.getElementById('messages-container').classList.add('hidden');
    document.getElementById('chat-interface').classList.remove('hidden');
    
    // Set recipient name
    document.querySelector('#chat-recipient span').textContent = matchName;
    
    // Load chat history
    loadChatMessages(matchId);
}

function closeChat() {
    currentChatMatch = null;
    document.getElementById('messages-container').classList.remove('hidden');
    document.getElementById('chat-interface').classList.add('hidden');
}

async function loadChatMessages(matchId) {
    try {
        const response = await fetch(`/api/chat/${matchId}`);
        const data = await response.json();
        
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML = data.messages.map(msg => `
            <div class="message ${msg.sender_name === currentUser ? 'sent' : 'received'}">
                <div class="message-content">
                    <p>${msg.content}</p>
                    <small>${new Date(msg.timestamp).toLocaleString()}</small>
                </div>
            </div>
        `).join('');
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    } catch (error) {
        console.error('Error loading chat messages:', error);
    }
}

// Load user settings
async function loadUserSettings() {
    try {
        const response = await fetch('/api/user-settings');
        const data = await response.json();
        
        if (response.ok) {
            // Populate basic preferences
            const basic = data.basic_preferences;
            document.getElementById('age').value = basic.age || '';
            document.getElementById('gender').value = basic.gender || '';
            document.getElementById('location').value = basic.location || '';
            document.getElementById('running_level').value = basic.running_level || '';
            document.getElementById('preferred_distance').value = basic.preferred_distance || '';
            document.getElementById('running_frequency').value = basic.running_frequency || '';
            document.getElementById('bio').value = basic.bio || '';
            document.getElementById('goals').value = basic.goals || '';
            
            // Populate running preferences
            const running = data.running_preferences;
            document.getElementById('preferred_pace').value = running.preferred_pace || '';
            document.getElementById('preferred_terrain').value = running.preferred_terrain || '';
            document.getElementById('race_participation').checked = running.race_participation || false;
            document.getElementById('group_runs').checked = running.group_runs || false;
        }
    } catch (error) {
        console.error('Error loading settings:', error);
    }
}

// Save user settings
async function saveUserSettings(event) {
    event.preventDefault();
    
    const formData = {
        basic_preferences: {
            age: parseInt(document.getElementById('age').value),
            gender: document.getElementById('gender').value,
            location: document.getElementById('location').value,
            running_level: document.getElementById('running_level').value,
            preferred_distance: document.getElementById('preferred_distance').value,
            running_frequency: document.getElementById('running_frequency').value,
            bio: document.getElementById('bio').value,
            goals: document.getElementById('goals').value
        },
        running_preferences: {
            preferred_pace: document.getElementById('preferred_pace').value,
            preferred_terrain: document.getElementById('preferred_terrain').value,
            race_participation: document.getElementById('race_participation').checked,
            group_runs: document.getElementById('group_runs').checked
        }
    };
    
    try {
        const response = await fetch('/api/user-settings', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            showNotification('Settings saved successfully!');
        } else {
            showNotification('Error saving settings', 'error');
        }
    } catch (error) {
        console.error('Error saving settings:', error);
        showNotification('Error saving settings', 'error');
    }
}

// Reset form to last saved settings
function resetForm() {
    loadUserSettings();
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Add event listeners
document.addEventListener('DOMContentLoaded', function() {
    const settingsForm = document.getElementById('settings-form');
    if (settingsForm) {
        settingsForm.addEventListener('submit', saveUserSettings);
    }
    
    // Load settings when settings section is shown
    const settingsLink = document.querySelector('a[data-section="settings"]');
    if (settingsLink) {
        settingsLink.addEventListener('click', loadUserSettings);
    }
});

// Function to handle opening the chat interface
function openChat(matchId, recipientName) {
    // Hide the messages container and show the chat interface
    document.getElementById('messages-container').classList.add('hidden');
    document.getElementById('chat-interface').classList.remove('hidden');
    
    // Update the chat recipient name
    document.querySelector('#chat-recipient span').textContent = recipientName;
    
    // Store the current match ID for sending messages
    document.getElementById('chat-form').dataset.matchId = matchId;
    
    // Load existing messages
    loadChatMessages(matchId);
}

// Function to handle closing the chat interface
function closeChat() {
    document.getElementById('chat-interface').classList.add('hidden');
    document.getElementById('messages-container').classList.remove('hidden');
}

// Function to load chat messages
async function loadChatMessages(matchId) {
    try {
        const response = await fetch(`/api/chat/${matchId}`);
        const data = await response.json();
        
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML = ''; // Clear existing messages
        
        data.messages.forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.className = `message ${message.sender_id === getCurrentUserId() ? 'sent' : 'received'}`;
            messageElement.innerHTML = `
                <div class="message-content">
                    <span class="sender">${message.sender_name}</span>
                    <p>${message.content}</p>
                    <span class="timestamp">${new Date(message.timestamp).toLocaleTimeString()}</span>
                </div>
            `;
            chatMessages.appendChild(messageElement);
        });
        
        // Scroll to the bottom of the messages
        chatMessages.scrollTop = chatMessages.scrollHeight;
    } catch (error) {
        console.error('Error loading messages:', error);
    }
}

// Add click event listeners to message buttons
document.addEventListener('DOMContentLoaded', () => {
    // Add event listeners to all message buttons
    const messageButtons = document.querySelectorAll('.message-button');
    messageButtons.forEach(button => {
        button.addEventListener('click', () => {
            const matchId = button.dataset.matchId;
            const recipientName = button.dataset.recipientName;
            openChat(matchId, recipientName);
        });
    });
    
    // Handle chat form submission
    const chatForm = document.getElementById('chat-form');
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        const matchId = chatForm.dataset.matchId;
        
        if (message) {
            try {
                const response = await fetch('/api/send-message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        match_id: matchId,
                        content: message
                    })
                });
                
                if (response.ok) {
                    input.value = '';
                    loadChatMessages(matchId); // Reload messages to show the new one
                }
            } catch (error) {
                console.error('Error sending message:', error);
            }
        }
    });
});

// Helper function to get current user ID
function getCurrentUserId() {
    // This should be implemented based on how you store the current user's ID
    // For example, you might store it in a data attribute on the body element
    return document.body.dataset.userId;
}