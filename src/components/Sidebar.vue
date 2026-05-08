<template>
    <button class="sidebar-toggle" @click="toggleSidebar">
        <div class="hamburger" :class="{ open: isOpen }">
            <span></span>
            <span></span>
            <span></span>
        </div>
    </button>

    <aside :class="['sidebar', { collapsed: !isOpen }]">

        <!-- MENU -->
        <div>

            <!-- HEADER -->
            <div class="menu-header">
                <h3>DriftDater</h3>
            </div>

            <!-- DISCOVER -->
            <router-link to="/discover" class="nav-item" :class="{ active: route.path === '/discover' }">
                <i class="fi fi-br-users"></i>
                <span>Browse</span>
            </router-link>
            
            <!-- SEARCH -->
            <router-link to="/search" class="nav-item" :class="{ active: route.path === '/search' }">
                <i class="fi fi-br-search"></i>
                <span>Search</span>
            </router-link>

            <!-- FAVOURITES -->
            <router-link to="/favourites" class="nav-item" :class="{ active: route.path === '/favourites' }">
                <i class="fi fi-br-bookmark"></i>
                <span>Favourites</span>
            </router-link>

            <!-- MATCHES -->
            <router-link to="/matches" class="nav-item" :class="{ active: route.path === '/matches' }">
                <i class="fi fi-br-heart"></i>
                <div class="nav-content">
                    <span>Matches</span>
                    <div v-if="matchNotifications > 0" class="notif-badge">
                        {{ matchNotifications }}
                    </div>
                </div>
            </router-link>

            <!-- MESSAGES -->
            <router-link to="/messages" class="nav-item" :class="{ active: route.path === '/messages' }">
                <i class="fi fi-br-messages"></i>
                <div class="nav-content">
                    <span>Messages</span>
                    <div v-if="messageNotifications > 0" class="notif-badge">
                        {{ messageNotifications }}
                    </div>
                </div>
            </router-link>

            <!-- PROFILE -->
            <router-link to="/profile" class="nav-item" :class="{ active: route.path === '/profile' }">
                <i class="fi fi-br-user"></i>
                <span>Profile</span>
            </router-link>
        </div>

        <!-- LOGOUT -->
        <button class="logout-btn" @click="logout">
            <i class="fi fi-br-sign-out-alt"></i>
            <span>Logout</span>
        </button>

    </aside>

    <!-- OVERLAY — closes sidebar when clicking outside -->
    <div v-if="isOpen" class="overlay" @click="isOpen = false"></div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import socket from '@/services/socket'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()

const isAuthenticated = computed(() => localStorage.getItem('isLoggedIn') === 'true')

// SIDEBAR
const isOpen = ref(false)

const toggleSidebar = () => {
    isOpen.value = !isOpen.value
}

watch(
    () => route.path,
    (newPath) => {
        isOpen.value = false

        if (newPath === '/messages') {
            messageNotifications.value = 0
        }
        if (newPath === '/matches') {
            matchNotifications.value = 0  // FIX: was matcheNotifications
        }
    }
)

// NOTIFICATIONS
const messageNotifications = ref(0)
const matchNotifications = ref(0)

const loadNotifications = async () => {
    if (!isAuthenticated.value) return
    try {
        const response = await api.get('/notifications')
        const notifications = response.data.notifications

        messageNotifications.value = notifications.filter(n =>
            n.message.toLowerCase().includes('message')
        ).length

        matchNotifications.value = notifications.filter(n =>
            n.message.toLowerCase().includes('match')
        ).length
    } catch (error) {
        console.error(error)
    }
}

onMounted(() => {
    loadNotifications()

    socket.on('new_message', () => { messageNotifications.value++ })
    socket.on('new_match',   () => { matchNotifications.value++ })
})

onUnmounted(() => {
    socket.off('new_message')
    socket.off('new_match')
})

// LOGOUT
const logout = async () => {
    try {
        await api.get('/auth/logout')
        localStorage.clear()
        router.push('/')
    } catch (error) {
        console.error(error)
    }
}
</script>

<style scoped>

/* OVERLAY */
.overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.3);
    z-index: 999;
    animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

/* SIDEBAR */
.sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 250px;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 30px 20px;
    background: linear-gradient(to bottom, #ff4d4d, #ff7a45);
    border-radius: 0 25px 25px 0;
    z-index: 1000;
    transform: translateX(0);
    transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1),
                box-shadow 0.35s ease;
    box-shadow: 4px 0 24px rgba(0,0,0,0.15);
}

.sidebar.collapsed {
    transform: translateX(-100%);
    box-shadow: none;
}

/* TOGGLE BUTTON */
.sidebar-toggle {
    position: fixed;
    top: 20px;
    left: 16px;
    z-index: 1001;
    width: 44px;
    height: 44px;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    transition: background 0.2s;
}

.sidebar-toggle:hover {
    background: rgba(0,0,0,0.05);
}

/* HAMBURGER ANIMATION */
.hamburger {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 24px;
    height: 18px;
}

.hamburger span {
    display: block;
    height: 2px;
    width: 100%;
    background: #333;
    border-radius: 2px;
    transition: transform 0.3s ease, opacity 0.3s ease, background 0.3s ease;
    transform-origin: center;
}

.hamburger.open span { background: white; }
.hamburger.open span:nth-child(1) { transform: translateY(8px) rotate(45deg); }
.hamburger.open span:nth-child(2) { opacity: 0; transform: scaleX(0); }
.hamburger.open span:nth-child(3) { transform: translateY(-8px) rotate(-45deg); }

/* MENU */
.menu-header {
    display: flex;
    align-items: center;
    gap: 12px;
    color: white;
    margin-top: 30px;
    margin-bottom: 30px;
    padding-left: 10px;
}

.menu-header h3 {
    font-size: 20px;
    font-weight: 700;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    color: white;
    text-decoration: none;
    padding: 12px 15px;
    border-radius: 14px;
    margin-bottom: 6px;
    font-size: 15px;
    font-weight: 500;
    transition: background 0.2s ease, transform 0.15s ease;
}

.nav-item:hover {
    background: rgba(255,255,255,0.18);
    transform: translateX(3px);
}

.nav-item.active {
    background: white;
    color: #ff4d4d;
    font-weight: 700;
}

.nav-item.active i { color: #ff4d4d; }

.nav-content {
    display: flex;
    align-items: center;
    gap: 10px;
}

.notif-badge {
    background: white;
    color: #ff4d4d;
    min-width: 20px;
    height: 20px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 700;
    animation: pop 0.3s cubic-bezier(0.36, 0.07, 0.19, 0.97);
}

@keyframes pop {
    0%   { transform: scale(0.5); opacity: 0; }
    70%  { transform: scale(1.2); }
    100% { transform: scale(1);   opacity: 1; }
}

.logout-btn {
    border: none;
    background: transparent;
    color: white;
    font-size: 15px;
    font-weight: 500;
    text-align: left;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 15px;
    border-radius: 14px;
    transition: background 0.2s ease;
    width: 100%;
}

.logout-btn:hover {
    background: rgba(255,255,255,0.18);
}
</style>