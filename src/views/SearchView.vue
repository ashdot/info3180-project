<template>

  <div class="search-page">

    <Sidebar />

    <div class="search-container">

      <!-- HEADER -->
      <div class="search-header">

        <h2>Discover</h2>

        <div class="search-row">

          <input
            v-model="first_name"
            type="text"
            placeholder="Search profiles..."
            class="search-bar"
            @keyup.enter="searchProfiles"
          />

          <button
            class="filter-btn"
            @click="showFilters = true"
          >
            ☰
          </button>

        </div>

      </div>

      <!-- FILTER -->
      <div
        v-if="showFilters"
        class="filter-overlay"
      >

        <div class="filter-modal">

          <!-- TOP -->
          <div class="filter-top">

            <button
              class="close-btn"
              @click="showFilters = false"
            >
              ✕
            </button>

            <h2>Filters</h2>

            <button
              class="clear-btn"
              @click="clearFilters"
            >
              Clear
            </button>

          </div>

          <!-- LOCATION -->
          <div class="filter-section">

            <label>Location</label>

            <div class="location-box">

              <input
                v-model="location"
                type="text"
                placeholder="Kingston, JA"
                class="location-input"
              />

              <span>></span>

            </div>

          </div>

          <!-- AGE -->
          <div class="filter-section">

            <div class="age-header">

              <label>Age</label>

              <p>{{ age }} years</p>

            </div>

            <input
              v-model="age"
              type="range"
              min="18"
              max="60"
              class="slider"
            />

          </div>

          <!-- INTERESTS -->
          <div class="filter-section">

            <label>Interested in</label>

            <div class="interest-tags">

              <button
                v-for="interest in [
                  'Tech',
                  'Music',
                  'Art',
                  'Sports',
                  'Cooking',
                  'Travel',
                  'Fitness',
                  'Gaming',
                  'Reading',
                  'Film',
                  'Photography',
                  'Fashion',
                  'Pets',
                  'Socializing'
                ]"
                :key="interest"
                :class="[
                  'tag',
                  selectedInterests.includes(interest)
                    ? 'active'
                    : ''
                ]"
                @click="toggleInterest(interest)"
              >
                {{ interest }}
              </button>

            </div>

          </div>

          <!-- BUTTON -->
          <button
            @click="searchProfiles"
            class="save-filter-btn"
          >
            Save Changes
          </button>

        </div>

      </div>

      <!-- SORT -->
      <div
        v-if="profiles.length > 0"
        class="sort-tabs"
      >

        <button
          :class="[
            'tab-btn',
            sort_by === 'all' ? 'active' : ''
          ]"
          @click="sort_by = 'all'"
        >
          All
        </button>

        <button
          :class="[
            'tab-btn',
            sort_by === 'newest' ? 'active' : ''
          ]"
          @click="sort_by = 'newest'"
        >
          Newest
        </button>

        <button
          :class="[
            'tab-btn',
            sort_by === 'most_similar' ? 'active' : ''
          ]"
          @click="sort_by = 'most_similar'"
        >
          Mutual
        </button>

      </div>

      <!-- PRE-SEARCH -->
      <div v-if="!searched" class="empty-state">
        <h2>Find Someone</h2>
        <p>Search by name, use filters, or just hit Search to browse everyone.</p>
      </div>

      <!-- NO RESULTS -->
      <div v-else-if="profiles.length === 0" class="empty-state">
        <h2>No Profiles Found</h2>
        <p>Try adjusting your search or filters.</p>
      </div>

      <!-- PROFILES -->
      <div v-if="profiles.length > 0" class="profiles-grid">

        <ProfileCard v-for="profile in profiles" :key="profile.user_id" :profile="profile">
          <template #actions>
            <button class="slot-btn view" @click="viewProfile(profile.user_id)">View Profile</button>
            <button class="slot-btn save" @click="saveProfile(profile.user_id)">Save</button>
          </template>
        </ProfileCard>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted} from 'vue'
import { useRouter } from 'vue-router'

import Sidebar from '@/components/Sidebar.vue'
import api from '@/services/api'
import ProfileCard from '@/components/ProfileCard.vue'

const first_name = ref('')
const location = ref('')
const age = ref(40)
const router = useRouter()

const sort_by = ref('newest')
const showFilters = ref(false)
const selectedInterests = ref([])
const profiles = ref([])
const searched = ref(false)

async function listProfiles() {
  try {
    const response = await api.get('/profile/all')
    profiles.value = response.data.profiles || []
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  listProfiles()
})

/* SEARCH */
const searchProfiles = async () => {
  try {
    const params = new URLSearchParams()

    if (first_name.value)                   params.append('first_name', first_name.value)
    if (location.value)                     params.append('location', location.value)
    if (selectedInterests.value.length)     params.append('interests', selectedInterests.value.join(','))
    params.append('max_age', age.value)
    params.append('sort_by', sort_by.value)

    // api baseURL is /api/v1 — backend route moved to /api/v1/search to match
    const response = await api.get(`/search?${params.toString()}`)

    profiles.value = response.data.profiles || []
    searched.value = true
    showFilters.value = false

  } catch (error) {
    console.error(error)
  }
}

/* INTEREST TOGGLE */
const toggleInterest = (interest) => {
  if (selectedInterests.value.includes(interest)) {
    selectedInterests.value = selectedInterests.value.filter(i => i !== interest)
  } else {
    selectedInterests.value.push(interest)
  }
}

/* CLEAR */
const clearFilters = () => {
  location.value = ''
  age.value = 40
  selectedInterests.value = []
}

const viewProfile = (user_id) => {
  router.push(`/profile/${user_id}`)
}

/* SAVE */
const saveProfile = async (user_id) => {
  try {
    const response = await api.post(`/profiles/${user_id}/save`)
    alert(response.data.message)
  } catch (error) {
    console.error(error)
  }
}
</script>

<style scoped>

.search-page {
  min-height: 100vh;
  background: #f5f5f7;
  padding: 40px 30px;
}

.search-container {
  max-width: 1200px;
  margin: auto;
  position: relative;
}

.search-header { margin-bottom: 35px; }

.search-header h2 {
  text-align: center;
  font-size: 36px;
  font-weight: 800;
  color: #111;
  margin-top: 20px;
  margin-bottom: 25px;
}

.search-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.search-bar {
  width: 100%;
  max-width: 900px;
  height: 58px;
  padding: 0 25px;
  border-radius: 40px;
  border: 1.5px solid #e0e0e0;
  background: white;
  font-size: 16px;
  box-sizing: border-box;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-bar:focus {
  outline: none;
  border-color: #ff4d4d;
  box-shadow: 0 2px 16px rgba(255,77,77,0.15);
}

.slot-btn {
  flex: 1;
  padding: 10px 14px;
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.slot-btn.view { background: #f8f8f8; color: #555; }
.slot-btn.view:hover { background: #ffe0e6; color: #ff4d4d; }
.slot-btn.save { background: linear-gradient(135deg, #ff4d4d, #ff7a45); color: white; }
.slot-btn.save:hover { opacity: 0.9; }

.filter-btn {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  border: 1.5px solid #e0e0e0;
  background: white;
  font-size: 22px;
  cursor: pointer;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.filter-btn:hover {
  background: #ffe0e6;
  border-color: #ff4d4d;
  color: #ff4d4d;
}

.filter-overlay {
  position: absolute;
  top: 130px;
  right: 40px;
  z-index: 1000;
}

.filter-modal {
  width: 420px;
  background: white;
  border-radius: 24px;
  padding: 28px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.12);
}

.filter-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
}

.filter-top h2 {
  font-size: 24px;
  font-weight: 800;
  margin: 0;
  color: #111;
}

.close-btn, .clear-btn {
  border: none;
  background: none;
  cursor: pointer;
}

.close-btn { font-size: 20px; color: #aaa; transition: color 0.2s; }
.close-btn:hover { color: #ff4d4d; }
.clear-btn { color: #bbb; font-size: 14px; font-weight: 600; transition: color 0.2s; }
.clear-btn:hover { color: #ff4d4d; }

.filter-section { margin-bottom: 28px; }

.filter-section label {
  display: block;
  font-size: 15px;
  font-weight: 700;
  color: #222;
  margin-bottom: 12px;
}

.location-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1.5px solid #eee;
  padding-bottom: 12px;
}

.location-input {
  border: none;
  outline: none;
  width: 100%;
  font-size: 15px;
  color: #555;
  background: transparent;
}

.age-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.age-header p { font-weight: 600; color: #ff4d4d; font-size: 15px; }

.slider { width: 100%; accent-color: #ff4d4d; }

.interest-tags { display: flex; flex-wrap: wrap; gap: 8px; }

.tag {
  padding: 8px 16px;
  border-radius: 30px;
  border: 1.5px solid #eee;
  background: white;
  color: #666;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s;
}

.tag:hover { border-color: #ff4d4d; color: #ff4d4d; }

.tag.active {
  background: linear-gradient(135deg, #ff4d4d, #ff7a45);
  color: white;
  border-color: transparent;
}

.save-filter-btn {
  width: 100%;
  height: 52px;
  border: none;
  border-radius: 30px;
  background: linear-gradient(135deg, #ff4d4d, #ff7a45);
  color: white;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.2s;
  box-shadow: 0 4px 14px rgba(255,77,77,0.3);
}

.save-filter-btn:hover { opacity: 0.9; transform: translateY(-1px); }

.empty-state { text-align: center; margin-top: 80px; }
.empty-state h2 { font-size: 36px; font-weight: 800; color: #222; margin-bottom: 10px; }
.empty-state p { font-size: 16px; color: #aaa; }

.sort-tabs { display: flex; justify-content: center; gap: 12px; margin-bottom: 35px; }

.tab-btn {
  border: none;
  padding: 10px 24px;
  border-radius: 30px;
  background: white;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: #555;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  transition: all 0.2s;
}

.tab-btn:hover { background: #ffe0e6; color: #ff4d4d; }

.tab-btn.active {
  background: linear-gradient(135deg, #ff4d4d, #ff7a45);
  color: white;
  box-shadow: 0 4px 14px rgba(255,77,77,0.3);
}

.profiles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

@media (max-width: 768px) {
  .search-header h2 { font-size: 28px; }
  .filter-overlay { right: 0; left: 0; display: flex; justify-content: center; }
  .filter-modal { width: 92%; }
  .profiles-grid { grid-template-columns: 1fr; }
}

</style>