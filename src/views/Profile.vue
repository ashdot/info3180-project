<template>
  <div class="layout">
    <Sidebar />

    <div class="profile-page">

      <!-- LOADING -->
      <div v-if="loading" class="state-msg">Loading profile...</div>

      <!-- ERROR -->
      <div v-else-if="error" class="state-msg error">{{ error }}</div>

      <div v-else-if="profile" class="profile-wrapper">

        <!-- CARD -->
        <div class="profile-card">

          <!-- BANNER + AVATAR -->
          <div class="banner">
            <div class="avatar-wrap">
              <img
                v-if="profile.photo"
                :src="profile.photo"
                :alt="profile.username"
                class="avatar"
              />
              <div v-else class="avatar avatar-placeholder">
                {{ profile.first_name?.charAt(0)?.toUpperCase() }}
              </div>
            </div>

            <button v-if="!isOwnProfile" class="edit-btn" @click="router.back()">Back</button>
          </div>

          <!-- INFO -->
          <div class="profile-body">

            <!-- Name / age / location -->
            <div class="identity">
              <h1 class="name">
                {{ profile.first_name }} {{ profile.last_name }}, {{ profile.age || '—' }}
              </h1>

              <div v-if="profile.location" class="meta-row">
                <span class="meta-icon">📍</span>
                <span>{{ profile.location }}</span>
              </div>

              <div v-if="profile.looking_for" class="badge">
                {{ formatLookingFor(profile.looking_for) }}
              </div>
            </div>

            <!-- ABOUT -->
            <section class="section">
              <h2 class="section-title">About</h2>
              <p class="bio-text">
                {{ profile.bio || 'No bio yet. Edit your profile to add one!' }}
              </p>
            </section>

            <!-- DETAILS -->
            <section v-if="profile.education" class="section">
              <h2 class="section-title">Details</h2>
              <div class="detail-row">
                <span class="detail-icon">🎓</span>
                <span>{{ profile.education }}</span>
              </div>
            </section>

            <!-- INTERESTS -->
            <section v-if="interestList.length" class="section">
              <h2 class="section-title">Interests</h2>
              <div class="tags">
                <span
                  v-for="interest in interestList"
                  :key="interest"
                  class="tag"
                >
                  {{ interest }}
                </span>
              </div>
            </section>

          </div>
        </div>

        <!-- STATS + VISIBILITY CARDS -->
        <div v-if="isOwnProfile" class="side-cards">

          <div class="side-card">
            <h3>Profile Visibility</h3>
            <div class="visibility-row">
              <span>Visibility</span>
              <span :class="['vis-badge', profile.visibility === 'Public' ? 'public' : 'private']">
                {{ profile.visibility }}
              </span>
            </div>
          </div>

          <div class="side-card">
            <h3>Quick Actions</h3>
            <button class="action-btn" @click="goToEdit">✏️ Edit Profile</button>
            <button class="action-btn" @click="$router.push('/search')">🔍 Discover</button>
            <button class="action-btn" @click="$router.push('/matches')">❤️ My Matches</button>
          </div>

        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import api from '@/services/api'

const router = useRouter()
const route = useRoute()

const profile = ref(null)
const loading = ref(true)
const error = ref('')

const isOwnProfile = computed(() => !route.params.user_id)

onMounted(async () => {
  try {
    const userid = route.params.user_id

    if (userid) {
      // Viewing someone else's profile
      const response = await api.get(`/profile/${userid}`)
      profile.value = response.data.data
    } else {
      // Viewing own profile
      const response = await api.get('/profile')
      profile.value = response.data
    }
  } catch (err) {
    error.value = 'Could not load profile.'
  } finally {
    loading.value = false
  }
})

// Parse interests — stored as comma-separated string or JSON array
const interestList = computed(() => {
  if (!profile.value?.interests) return []
  try {
    const parsed = JSON.parse(profile.value.interests)
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return profile.value.interests.split(',').map(i => i.trim()).filter(Boolean)
  }
})

const formatLookingFor = (val) => {
  const map = {
    long_term: 'Long-term Relationship',
    casual: 'Casual / Hookups',
    friendship: 'Friendship / Companionship',
    flow: 'Going with the Flow',
  }
  return map[val] || val
}

const goToEdit = () => router.push('/edit-profile')
</script>

<style scoped>

.layout {
  display: flex;
  min-height: 100vh;
  background: #f5f5f7;
}

.profile-page {
  flex: 1;
  padding: 40px 40px 40px 40px;
  max-width: 1100px;
  margin: 0 auto;
  width: 100%;
}

/* Loading / error */
.state-msg {
  text-align: center;
  margin-top: 80px;
  font-size: 18px;
  color: #888;
}
.state-msg.error { color: #e05; }

/* Layout */
.profile-wrapper {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 24px;
  align-items: start;
}

/* CARD */
.profile-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 28px rgba(0,0,0,0.08);
  overflow: hidden;
}

/* BANNER */
.banner {
  height: 180px;
  background: linear-gradient(to right, #ff4d4d, #ff7a45);
  position: relative;
}

.avatar-wrap {
  position: absolute;
  bottom: -50px;
  left: 32px;
}

.avatar {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  border: 4px solid white;
  object-fit: cover;
  background: #eee;
  display: block;
}

.avatar-placeholder {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  border: 4px solid white;
  background: #ffccd5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  font-weight: 700;
  color: #ff4d4d;
}

.edit-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: white;
  border: none;
  border-radius: 10px;
  padding: 8px 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
  transition: box-shadow 0.2s;
}

.edit-btn:hover { box-shadow: 0 4px 14px rgba(0,0,0,0.18); }

/* BODY */
.profile-body {
  padding: 70px 32px 32px;
}

.identity { margin-bottom: 24px; }

.name {
  font-size: 28px;
  font-weight: 800;
  margin-bottom: 8px;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #555;
  margin-bottom: 10px;
  font-size: 15px;
}

.badge {
  display: inline-block;
  background: #ffe0e6;
  color: #ff4d4d;
  border-radius: 20px;
  padding: 4px 14px;
  font-size: 13px;
  font-weight: 600;
}

/* SECTIONS */
.section { margin-bottom: 24px; }

.section-title {
  font-size: 17px;
  font-weight: 700;
  margin-bottom: 10px;
  color: #222;
}

.bio-text {
  color: #555;
  line-height: 1.6;
  font-size: 15px;
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #555;
  font-size: 15px;
}

/* INTERESTS */
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background: #ffe0e6;
  color: #ff4d4d;
  border-radius: 20px;
  padding: 6px 14px;
  font-size: 13px;
  font-weight: 500;
}

/* SIDE CARDS */
.side-cards {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.side-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.07);
  padding: 22px;
}

.side-card h3 {
  font-size: 15px;
  font-weight: 700;
  margin-bottom: 14px;
  color: #222;
}

.visibility-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: #555;
}

.vis-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
}

.vis-badge.public  { background: #d1fae5; color: #065f46; }
.vis-badge.private { background: #fee2e2; color: #991b1b; }

.action-btn {
  width: 100%;
  text-align: left;
  background: #f8f8f8;
  border: none;
  border-radius: 10px;
  padding: 10px 14px;
  font-size: 14px;
  cursor: pointer;
  margin-bottom: 8px;
  transition: background 0.2s;
}

.action-btn:hover { background: #ffe0e6; color: #ff4d4d; }
.action-btn:last-child { margin-bottom: 0; }

/* RESPONSIVE */
@media (max-width: 768px) {
  .profile-wrapper {
    grid-template-columns: 1fr;
  }
  .profile-page {
    padding: 20px 16px;
  }
}
</style>
