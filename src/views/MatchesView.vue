<template>
    <div class="layout">
  
        <Sidebar />
  
        <main class="page-content">
  
            <div class="heading">
                <h2>Matches</h2>
            </div>
  
            <div class="filters">
  
                <button
                    :class="{ active: filter === 'all' }"
                    @click="filter = 'all'"
                >
                    All
                </button>
  
                <button
                    :class="{ active: filter === 'newest' }"
                    @click="filter = 'newest'"
                >
                    Newest
                </button>
  
                <button
                    :class="{ active: filter === 'mutual' }"
                    @click="filter = 'mutual'"
                >
                    Mutual
                </button>
  
            </div>
  
            <div class="match-grid">
                <div v-for="match in filteredMatches" :key="match.id" class="match-card">
                 <div>   
                    <img :src="match.photo" class="match-img"/>
                </div>
                <div class="overlay">
                    <div class="match-info">
                        <h2>
                            {{ match.first_name }}
                            {{ match.last_name }},
                            {{ match.age || '—' }}
                        </h2>
                        <p>{{ match.bio }}</p>
                        <button class="btn-profile" @click="viewProfile(match.user_id)">View Profile</button>
                        <button class="btn-message" @click="goToMessages(match.match_id)">Message</button>
                    </div>
                </div>
            </div>   
        </div>
    </main>
    </div>
</template>
  
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import Sidebar from '@/components/Sidebar.vue'
 
const router = useRouter()
const matches = ref([])
const filter = ref('all')
const loading = ref(true)
 
onMounted(async () => {
    try {
        const response = await api.get('/matches')
        matches.value = response.data.matches || []
    } catch (error) {
        console.error(error)
    } finally {
        loading.value = false
    }
})

const filteredMatches = computed(() => {
    if (filter.value === 'newest') {
        return [...matches.value].reverse()
    }
    return matches.value
})

const viewProfile = (user_id) => {
    router.push(`/profile/${user_id}`)
}
 
const goToMessages = (match_id) => {
    router.push(`/messages/${match_id}`)
}
</script>
  
<style scoped>
 
.layout {
    display: flex;
    min-height: 100vh;
    background: #f5f5f7;
}

.page-content {
    flex: 1;
    padding: 40px 60px;
    max-width: 1200px;
    margin: 0 auto;
}

.heading {
    display: flex;
    justify-content: center;
    margin-top: 20px;
    margin-bottom: 10px;
}

.heading h2 {
    font-size: 36px;
    font-weight: 800;
    color: #111;
}

.filters {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-bottom: 40px;
}
  
.filters button {
    border: none;
    background: white;
    padding: 10px 24px;
    border-radius: 999px;
    cursor: pointer;
    font-weight: 600;
    font-size: 14px;
    color: #555;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    transition: all 0.2s;
}

.filters button:hover {
    background: #ffe0e6;
    color: #ff4d4d;
}
  
.filters button.active {
    background: linear-gradient(to right, #ff4d4d, #ff7a45);
    color: white;
    box-shadow: 0 4px 14px rgba(255,77,77,0.3);
}
  
.match-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 24px;
}
  
.match-card {
    position: relative;
    height: 380px;
    border-radius: 20px;
    overflow: hidden;
    cursor: pointer;
    box-shadow: 0 4px 20px rgba(0,0,0,0.10);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.match-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.15);
}
  
.match-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: top;
}
  
.overlay {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 18px;
    background: linear-gradient(to top, rgba(0,0,0,0.75), transparent 55%);
}
  
.match-info h2 {
    color: white;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 4px;
}

.match-info p {
    color: rgba(255,255,255,0.75);
    font-size: 13px;
    margin-bottom: 12px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.btn-profile,
.btn-message {
    padding: 9px 16px;
    border: none;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    margin-right: 8px;
}

.btn-profile {
    background: rgba(255,255,255,0.2);
    color: white;
    border: 1px solid rgba(255,255,255,0.35);
    backdrop-filter: blur(4px);
}

.btn-profile:hover {
    background: rgba(255,255,255,0.35);
}

.btn-message {
    background: white;
    color: #ff4d4d;
}

.btn-message:hover {
    background: #ffe0e6;
}

@media (max-width: 768px) {
    .page-content { padding: 20px 16px; }
    .match-grid { grid-template-columns: 1fr; }
}
</style>