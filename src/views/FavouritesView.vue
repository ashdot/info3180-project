<template>
    <div class="layout">
  
        <Sidebar />
  
        <main class="page-content">
  
            <div class="heading">
                <h2>Saved Profiles</h2>
            </div>
 
            <div v-if="loading" class="state-msg">Loading...</div>
 
            <div v-else-if="savedProfiles.length === 0" class="empty-state">
                <p>No saved profiles yet. Save profiles you like while browsing!</p>
            </div>
  
            <div v-else class="favourites-grid">
                <ProfileCard
                    v-for="profile in savedProfiles"
                    :key="profile.user_id"
                    :profile="profile"
                >
                    <template #actions>
                        <button class="slot-btn view" @click="viewProfile(profile.user_id)">View</button>
                        <button class="slot-btn unsave" @click="unsaveProfile(profile.user_id)">Unsave</button>
                    </template>
                </ProfileCard>
            </div>
        </main>
    </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import Sidebar from '@/components/Sidebar.vue'
import ProfileCard from '@/components/ProfileCard.vue'
 
const router = useRouter()
const savedProfiles = ref([])
const loading = ref(true)
 
onMounted(async () => {
    try {
        const response = await api.get('/profiles/saved')
        savedProfiles.value = response.data.saved_profiles || []
    } catch (error) {
        console.error(error)
    } finally {
        loading.value = false
    }
})
 
const viewProfile = (user_id) => {
    router.push(`/profile/${user_id}`)
}
 
const unsaveProfile = async (user_id) => {
    try {
        await api.post(`/profiles/${user_id}/save`)
        savedProfiles.value = savedProfiles.value.filter(p => p.user_id !== user_id)
    } catch (error) {
        console.error(error)
    }
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
    margin-bottom: 30px;
}

.heading h2 {
    font-size: 36px;
    font-weight: 800;
    color: #111;
}

.state-msg {
    text-align: center;
    margin-top: 80px;
    color: #aaa;
    font-size: 16px;
}

.empty-state {
    text-align: center;
    margin-top: 80px;
    color: #aaa;
    font-size: 16px;
}

.favourites-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 24px;
}

:deep(.slot-btn) {
  flex: 1;
  padding: 10px 14px;
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

:deep(.slot-btn.view) { background: #f8f8f8; color: #555; }
:deep(.slot-btn.view:hover) { background: #ffe0e6; color: #ff4d4d; }
:deep(.slot-btn.unsave) { background: linear-gradient(135deg, #ff4d4d, #ff7a45); color: white; }
:deep(.slot-btn.unsave:hover) { opacity: 0.9; }
</style>