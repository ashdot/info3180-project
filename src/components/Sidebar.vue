<template>
    <button class="sidebar-toggle" @click="toggleSidebar">
        <i 
            class="fi fi-br-menu-burger"
            :class="{ open: isOpen }"
        ></i>
    </button>

    <aside :class="['sidebar', { collapsed: !isOpen }]">

        <!-- MENU -->
        <div>

            <!-- HEADER -->
            <div class="menu-header">
                <h3>Menu</h3>
            </div>

            <!-- DISCOVER -->
            <router-link
                to="/search"
                class="nav-item"
                :class="{ active: route.path === '/search' }"
            >
                <i class="fi fi-br-search"></i>
                <span>Discover</span>
            </router-link>

            <!-- FAVOURITES -->
            <router-link
                to="/favourites"
                class="nav-item"
                :class="{ active: route.path === '/favourites' }"
            >
                <i class="fi fi-br-bookmark"></i>
                <span>Favourites</span>
            </router-link>

            <!-- MATCHES -->
            <router-link
                to="/matches"
                class="nav-item"
                :class="{ active: route.path === '/matches' }"
            >
                <i class="fi fi-br-heart"></i>

                <div class="nav-content">
                    <span>Matches</span>

                    <div
                        v-if="matchNotifications > 0"
                        class="notif-badge"
                    >
                        {{ matchNotifications }}
                    </div>
                </div>
            </router-link>

            <!-- MESSAGES -->
            <router-link
                to="/messages"
                class="nav-item"
                :class="{ active: route.path === '/messages' }"
            >
                <i class="fi fi-br-messages"></i>

                <div class="nav-content">
                    <span>Messages</span>

                    <div
                        v-if="messageNotifications > 0"
                        class="notif-badge"
                    >
                        {{ messageNotifications }}
                    </div>
                </div>
            </router-link>

            <!-- PROFILE -->
            <router-link
                to="/edit-profile"
                class="nav-item"
                :class="{ active: route.path === '/edit-profile' }"
            >
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
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import socket from '@/services/socket'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()

// AUTH
const isAuthenticated = computed(() => {
    return !!localStorage.getItem('token')
})

// SIDEBAR
const isOpen = ref(false)

const toggleSidebar = () => {
    isOpen.value = !isOpen.value
}

watch(
    () => route.path,
    () => {
        isOpen.value = false
    }
)

// NOTIFICATIONS
const messageNotifications = ref(0)
const matchNotifications = ref(0)

// LOAD INITIAL NOTIFICATIONS
const loadNotifications = async () => {

    try {

        const response = await api.get('/notifications')

        const notifications = response.data.notifications

        messageNotifications.value =
            notifications.filter(n =>
                n.message.toLowerCase().includes('message')
            ).length

        matchNotifications.value =
            notifications.filter(n =>
                n.message.toLowerCase().includes('match')
            ).length

    } catch (error) {
        console.error(error)
    }
}

// SOCKET LISTENERS
onMounted(() => {

    loadNotifications()

    socket.on('new_message', () => {
        messageNotifications.value++
    })

    socket.on('new_match', () => {
        matchNotifications.value++
    })
})

onUnmounted(() => {
    socket.off('new_message')
    socket.off('new_match')
})

// LOGOUT
const logout = async () => {
    
    try {

        await api.get('/auth/logout')

    } catch (error) {

        console.error(error)

    } finally {

        localStorage.removeItem('token')
        localStorage.removeItem('user_id')

        alert('Logged out successfully')

        router.push('/')

    }
}
</script>

<style scoped>

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

    background: linear-gradient(
        to bottom,
        #ff4d4d,
        #ff7a45
    );

    border-radius: 0 25px 25px 0;

    transform: translateX(0);
    transition: transform 0.3s ease;

    z-index: 1000;
}

.sidebar-toggle {
    position: fixed;
    top: 40px;
    left: 20px;

    z-index: 1001;

    margin-top: 15px;
    margin-left: 5px;

    width: 50px;
    height: 50px;

    border: none;
    border-radius: 10px;

    cursor: pointer;

    display: flex;
    align-items: center;
    justify-content: center;

    background: transparent;
}

.sidebar.collapsed {
    transform: translateX(-100%);
}

.sidebar-toggle i {
    font-size: 20px;
    color: black;
    transition: color 0.3s ease;
}

.sidebar-toggle i.open {
    color: white;
}

.menu-header {
    display: flex;
    align-items: center;
    gap: 12px;

    color: white;

    margin-top: 30px;
    margin-bottom: 30px;

    padding-left: 50px;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;

    color: white;
    text-decoration: none;

    padding: 12px 15px;
    border-radius: 14px;

    margin-bottom: 10px;

    transition: 0.2s ease;
}

.nav-item:hover {
    background: rgba(255,255,255,0.15);
}

.nav-item.active {
    background: white;
    color: #111;
}

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

    font-size: 12px;
    font-weight: bold;
}

.logout-btn {
    border: none;
    background: transparent;

    color: white;
    font-size: 16px;

    text-align: left;
    cursor: pointer;

    display: flex;
    align-items: center;
    gap: 12px;

    padding: 12px 15px;
    border-radius: 14px;

    transition: 0.2s ease;
}

.logout-btn:hover {
    background: rgba(255,255,255,0.15);
}
</style>