<template>
    <div class="layout">
        
        <Sidebar />

        <main class="page-content">
            
            <div class="heading">
                <h2>Messages</h2>
            </div>

            <div v-if="loading" class="state-msg">Loading...</div>

            <div v-else-if="matches.length === 0" class="empty-state">
                <p>No matches yet. Match with someone to start messaging!</p>
            </div>

            <div
                v-for="match in matches"
                :key="match.match_id"
                class="conversation"
                :class="{ active: activeMatchId === match.match_id }"
                @click="openChat(match.match_id)"
            >
                <div class="avatar-wrap">
                    <img v-if="match.photo" :src="match.photo" class="avatar" />
                    <div v-else class="avatar avatar-placeholder">
                        {{ match.first_name?.charAt(0)?.toUpperCase() }}
                    </div>
                </div>

                <div class="conversation-info">
                    <h2>{{ match.first_name }} {{ match.last_name }}</h2>
                    <p v-if="match.location" class="sub">📍 {{ match.location }}</p>
                </div>

                <span class="arrow">›</span>
            </div>
        </main>

        <!-- CHAT PANEL -->
        <aside v-if="activeMatchId" class="chat-panel">

            <div class="chat-header">
                <button class="back-btn" @click="activeMatchId = null">←</button>
                <h3>{{ activeName }}</h3>
            </div>

            <div class="chat-messages" ref="messageContainer">
                <div v-if="messages.length === 0" class="no-messages">
                    No messages yet. Say hello! 👋
                </div>
                <div
                    v-for="msg in messages"
                    :key="msg.message_id"
                    :class="['bubble', msg.sender === currentUsername ? 'mine' : 'theirs']"
                >
                    <p>{{ msg.content }}</p>
                    <span class="time">{{ formatTime(msg.timestamp) }}</span>
                </div>
            </div>

            <div class="chat-input">
                <input
                    v-model="newMessage"
                    type="text"
                    placeholder="Type a message..."
                    @keyup.enter="sendMessage"
                />
                <button @click="sendMessage">Send</button>
            </div>

        </aside>

        <!-- PLACEHOLDER when no chat selected -->
        <aside v-else class="chat-panel chat-placeholder">
            <p>Select a match to start chatting</p>
        </aside>

    </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/api'
import Sidebar from '@/components/Sidebar.vue'

const route = useRoute()

const matches         = ref([])
const messages        = ref([])
const activeMatchId   = ref(null)
const newMessage      = ref('')
const loading         = ref(true)
const messageContainer = ref(null)

const currentUsername = localStorage.getItem('username')

onMounted(async () => {
    try {
        const response = await api.get('/matches')
        matches.value = response.data.matches || []

        // FIX: if navigated to /messages/:match_id open that chat automatically
        const matchId = route.params.match_id
        if (matchId) {
            await openChat(Number(matchId))
        }
    } catch (error) {
        console.error(error)
    } finally {
        loading.value = false
    }
})

const activeName = computed(() => {
    const match = matches.value.find(m => m.match_id === activeMatchId.value)
    return match ? `${match.first_name} ${match.last_name}` : ''
})

const openChat = async (match_id) => {
    activeMatchId.value = match_id
    messages.value = []
    try {
        const response = await api.get(`/messages/${match_id}`)
        messages.value = response.data.messages || []
        await nextTick()
        scrollToBottom()
    } catch (error) {
        console.error(error)
    }
}

const sendMessage = async () => {
    if (!newMessage.value.trim() || !activeMatchId.value) return

    try {
        await api.post(`/messages/${activeMatchId.value}`, {
            message: newMessage.value
        })
        newMessage.value = ''
        const response = await api.get(`/messages/${activeMatchId.value}`)
        messages.value = response.data.messages || []
        await nextTick()
        scrollToBottom()
    } catch (error) {
        console.error(error)
    }
}

const scrollToBottom = () => {
    if (messageContainer.value) {
        messageContainer.value.scrollTop = messageContainer.value.scrollHeight
    }
}

const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>

.layout {
    display: flex;
    min-height: 100vh;
    background: #f5f5f7;
}

/* LEFT PANEL */
.page-content {
    width: 360px;
    flex-shrink: 0;
    background: white;
    border-right: 1px solid #eee;
    padding: 20px 0;
    overflow-y: auto;
}

.heading {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    margin-bottom: 10px;
}

.heading h2 {
    font-size: 24px;
    font-weight: 800;
}

.state-msg, .empty-state {
    text-align: center;
    padding: 40px 20px;
    color: #888;
    font-size: 15px;
}

.conversation {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 20px;
    cursor: pointer;
    transition: background 0.2s;
    border-bottom: 1px solid #f5f5f5;
}

.conversation:hover { background: #fdf2f8; }
.conversation.active { background: #ffe0e6; }

.avatar {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    object-fit: cover;
    object-position: top;
    flex-shrink: 0;
}

.avatar-placeholder {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ff4d4d, #ff7a45);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    font-weight: 700;
    color: white;
    flex-shrink: 0;
}

.conversation-info { flex: 1; }

.conversation-info h2 {
    font-size: 16px;
    font-weight: 700;
    color: #111;
    margin-bottom: 2px;
}

.sub {
    font-size: 13px;
    color: #999;
}

.arrow {
    font-size: 20px;
    color: #ccc;
}

/* CHAT PANEL */
.chat-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: white;
    min-height: 100vh;
}

.chat-placeholder {
    align-items: center;
    justify-content: center;
    color: #aaa;
    font-size: 16px;
}

.chat-header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 18px 24px;
    border-bottom: 1px solid #eee;
    background: white;
    position: sticky;
    top: 0;
}

.back-btn {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    color: #ff4d4d;
    padding: 4px 8px;
    border-radius: 8px;
    transition: background 0.2s;
}

.back-btn:hover { background: #ffe0e6; }

.chat-header h3 {
    font-size: 18px;
    font-weight: 700;
}

.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.no-messages {
    text-align: center;
    color: #aaa;
    margin-top: 40px;
    font-size: 15px;
}

.bubble {
    max-width: 60%;
    padding: 10px 14px;
    border-radius: 18px;
    font-size: 15px;
    line-height: 1.5;
    animation: fadeUp 0.2s ease;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

.bubble.mine {
    align-self: flex-end;
    background: linear-gradient(135deg, #ff4d4d, #ff7a45);
    color: white;
    border-bottom-right-radius: 4px;
}

.bubble.theirs {
    align-self: flex-start;
    background: #f0f0f0;
    color: #111;
    border-bottom-left-radius: 4px;
}

.bubble p { margin: 0; }

.time {
    font-size: 11px;
    opacity: 0.6;
    display: block;
    margin-top: 4px;
    text-align: right;
}

.chat-input {
    display: flex;
    gap: 10px;
    padding: 16px 24px;
    border-top: 1px solid #eee;
    background: white;
    position: sticky;
    bottom: 0;
}

.chat-input input {
    flex: 1;
    padding: 12px 18px;
    border: 1px solid #ddd;
    border-radius: 30px;
    font-size: 15px;
    outline: none;
    transition: border-color 0.2s;
}

.chat-input input:focus { border-color: #ff4d4d; }

.chat-input button {
    padding: 12px 24px;
    background: linear-gradient(135deg, #ff4d4d, #ff7a45);
    color: white;
    border: none;
    border-radius: 30px;
    font-weight: 600;
    font-size: 15px;
    cursor: pointer;
    transition: opacity 0.2s;
}

.chat-input button:hover { opacity: 0.9; }
</style>