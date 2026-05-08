<template>
  <div class="layout">
    <Sidebar />
 
    <div class="discover-page">
 
      <div class="heading">
        <h1>Discover</h1>
        <p>Find your perfect match based on your preferences</p>
      </div>
 
      <!-- LOADING -->
      <div v-if="loading" class="state-msg">Loading profiles...</div>
 
      <!-- NO MORE PROFILES -->
      <div v-else-if="profiles.length === 0" class="empty-state">
        <p class="text-lg text-gray-500">No more profiles to show</p>
        <button class="restart-btn" @click="loadProfiles">Refresh</button>
      </div>
 
      <!-- CURRENT PROFILE CARD -->
      <div v-else class="card-wrap">
 
        <ProfileCard :profile="currentProfile">
          <template #actions>
            <div style="display: flex; gap: 16px; justify-content: center; margin-top: 12px;">
              <button class="action-btn dislike" @click="handleDislike" title="Pass"><i class="fi fi-br-cross"></i></button>
              <button class="action-btn save" @click="handleSave" title="Save"><i class="fi fi-br-bookmark"></i></button>
              <button class="action-btn like" @click="handleLike" title="Like"><i class="fi fi-br-heart "></i></button>
            </div>
          </template>
        </ProfileCard>
 
        <!-- COUNTER -->
        <p class="counter">
          {{ currentIndex + 1 }} of {{ profiles.length }}
        </p>
 
      </div>
 
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import ProfileCard from '@/components/ProfileCard.vue'
import api from '@/services/api'
 
const router = useRouter()
 
const profiles    = ref([])
const currentIndex = ref(0)
const loading     = ref(true)

const currentProfile = computed(() => {
  const p = profiles.value[currentIndex.value]
  if (!p) return null

  return {
    ...p,
    photo_url: p.photo_url
      ? `${BASE_URL}/uploads/${p.photo_url}`
      : null
  }
})
 
const loadProfiles = async () => {
  loading.value = true
  try {
    const response = await api.get('/discover')
    profiles.value = response.data.matches || []
    currentIndex.value = 0
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}
 
onMounted(() => loadProfiles())
 
const next = () => {
  if (currentIndex.value < profiles.value.length - 1) {
    currentIndex.value++
  } else {
    profiles.value = []
  }
}


 
const handleLike = async () => {
  try {
    const response = await api.post(`/profiles/${currentProfile.value.user_id}/like`)
    if (response.data.match_id) {
      alert(`🎉 You matched with ${currentProfile.value.first_name}!`)
    }
    next()
  } catch (error) {
    console.error(error)
  }
}
 
const handleDislike = async () => {
  try {
    await api.post(`/profiles/${currentProfile.value.user_id}/dislike`)
    next()
  } catch (error) {
    console.error(error)
  }
}
 
const handleSave = async () => {
  try {
    const response = await api.post(`/profiles/${currentProfile.value.user_id}/save`)
    alert(response.data.message)
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

.discover-page {
  flex: 1;
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.heading {
  text-align: center;
  margin-bottom: 32px;
}

.heading h1 {
  font-size: 36px;
  font-weight: 800;
  color: #111;
  margin-bottom: 6px;
}

.heading p {
  color: #999;
  font-size: 15px;
}

.state-msg {
  font-size: 18px;
  color: #aaa;
  margin-top: 80px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin-top: 80px;
}

.empty-state .text-lg {
  font-size: 18px;
  color: #aaa;
}

.restart-btn {
  padding: 12px 32px;
  background: linear-gradient(135deg, #ff4d4d, #ff7a45);
  color: white;
  border: none;
  border-radius: 30px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.2s;
}

.restart-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.card-wrap {
  position: relative;
  width: 100%;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.counter {
  color: #aaa;
  font-size: 14px;
}

/* ACTION BUTTONS */
.action-btn {
  width: 56px;
  height: 56px;
  font-size: 22px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 4px 14px rgba(0,0,0,0.12);
}

.action-btn:hover {
  transform: scale(1.12);
  box-shadow: 0 6px 20px rgba(0,0,0,0.18);
}

.action-btn.dislike {
  background: white;
  color: #e74c3c;
  border: 2px solid #e74c3c;
}

.action-btn.dislike:hover {
  background: #e74c3c;
  color: white;
}

.action-btn.save {
  background: white;
  color: #ff7a45;
  border: 2px solid #ff7a45;
}

.action-btn.save:hover {
  background: #ff7a45;
  color: white;
}

.action-btn.like {
  background: white;
  color: #ff4d4d;
  border: 2px solid #ff4d4d;
}

.action-btn.like:hover {
  background: #ff4d4d;
  color: white;
}
</style>