<template>

  <div class="search-page">

    <Sidebar />

    <div class="search-container">

      <!-- HEADER -->
      <div class="search-header">

        <h1>Discover</h1>

        <div class="search-row">

          <input
            v-model="first_name"
            type="text"
            placeholder="Search profiles..."
            class="search-bar"
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

      <!-- EMPTY -->
      <div
        v-if="profiles.length === 0"
        class="empty-state"
      >

        <h2>No Profiles Yet</h2>

        <p>
          Profiles will appear here after users sign up.
        </p>

      </div>

      <!-- PROFILES -->
      <div
        v-else
        class="profiles-grid"
      >

        <div
          v-for="profile in profiles"
          :key="profile.user_id"
          class="profile-card"
        >

          <div class="match-tag">
            {{ profile.score || 70 }}% Match
          </div>

          <img
            :src="profile.photo"
            class="profile-img"
          />

          <div class="profile-overlay">

            <h3>
              {{ profile.username }},
              {{ profile.age }}
            </h3>

            <p class="location-text">
              📍 {{ profile.location }}
            </p>

          </div>

          <button
            @click="saveProfile(profile.user_id)"
            class="save-btn"
          >
            Save
          </button>

        </div>

      </div>

    </div>

  </div>

</template>

<script setup>
import { ref } from 'vue'

import Sidebar from '@/components/Sidebar.vue'

const first_name = ref('')
const location = ref('')
const age = ref(25)

const sort_by = ref('newest')

const showFilters = ref(false)

const selectedInterests = ref([])

const profiles = ref([])

/* SEARCH */
const searchProfiles = async () => {

  try {

    const params = new URLSearchParams({
      first_name: first_name.value,
      location: location.value,
      age: age.value,
      interests: selectedInterests.value.join(','),
      sort_by: sort_by.value
    })

    const response = await fetch(
      `http://127.0.0.1:5000/api/search?${params.toString()}`
    )

    const data = await response.json()

    profiles.value = data.profiles || []

    showFilters.value = false

  } catch (error) {

    console.log(error)

  }
}

/* INTEREST TOGGLE */
const toggleInterest = (interest) => {

  if(selectedInterests.value.includes(interest)){

    selectedInterests.value =
      selectedInterests.value.filter(
        item => item !== interest
      )

  } else {

    selectedInterests.value.push(interest)

  }
}

/* CLEAR */
const clearFilters = () => {

  location.value = ''

  age.value = 25

  selectedInterests.value = []

}

/* SAVE */
const saveProfile = async (user_id) => {

  try {

    const response = await fetch(
      `http://127.0.0.1:5000/api/v1/profiles/${user_id}/save`,
      {
        method: 'POST',
        credentials: 'include'
      }
    )

    const data = await response.json()

    alert(data.message)

  } catch (error) {

    console.log(error)

  }
}
</script>

<style scoped>

.search-page{
  min-height: 100vh;
  background: #f5f5f5;
  padding: 40px 30px;
}

.search-container{
  max-width: 1200px;
  margin: auto;
  position: relative;
}

/* HEADER */

.search-header{
  margin-bottom: 35px;
}

.search-header h1{
  text-align: center;
  font-size: 48px;
  font-weight: 700;
  color: #222;
  margin-bottom: 25px;
}

/* SEARCH */

.search-row{
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.search-bar{
  width: 100%;
  max-width: 900px;

  height: 60px;

  padding: 0 25px;

  border-radius: 40px;

  border: 1px solid #ddd;

  background: white;

  font-size: 18px;

  box-sizing: border-box;
}

.search-bar:focus{
  outline: none;
  border-color: #e86b56;
}

.filter-btn{
  width: 60px;
  height: 60px;

  border-radius: 50%;

  border: 1px solid #ddd;

  background: white;

  font-size: 24px;

  cursor: pointer;

  transition: 0.3s;
}

.filter-btn:hover{
  background: #f3f3f3;
}

/* FILTER PANEL */

.filter-overlay{
  position: absolute;

  top: 130px;
  right: 40px;

  z-index: 1000;
}

.filter-modal{
  width: 420px;

  background: white;

  border-radius: 20px;

  padding: 25px;

  box-shadow: 0 10px 40px rgba(0,0,0,0.15);
}

.filter-top{
  display: flex;
  justify-content: space-between;
  align-items: center;

  margin-bottom: 25px;
}

.filter-top h2{
  font-size: 32px;
  margin: 0;
}

.close-btn,
.clear-btn{
  border: none;
  background: none;
  cursor: pointer;
}

.close-btn{
  font-size: 28px;
}

.clear-btn{
  color: #aaa;
  font-size: 16px;
}

.filter-section{
  margin-bottom: 30px;
}

.filter-section label{
  display: block;

  font-size: 22px;
  font-weight: 700;

  margin-bottom: 12px;
}

/* LOCATION */

.location-box{
  display: flex;
  align-items: center;
  justify-content: space-between;

  border-bottom: 1px solid #ddd;

  padding-bottom: 12px;
}

.location-input{
  border: none;
  outline: none;

  width: 100%;

  font-size: 18px;

  color: #777;
}

/* AGE */

.age-header{
  display: flex;
  justify-content: space-between;
  align-items: center;

  margin-bottom: 15px;
}

.slider{
  width: 100%;
  accent-color: #e86b56;
}

/* TAGS */

.interest-tags{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag{
  padding: 10px 18px;

  border-radius: 30px;

  border: 1px solid #e86b56;

  background: white;

  color: #666;

  cursor: pointer;

  font-size: 15px;

  transition: 0.3s;
}

.tag.active{
  background: linear-gradient(
    135deg,
    #e86b56,
    #f09b5f
  );

  color: white;
}

/* BUTTON */

.save-filter-btn{
  width: 100%;
  height: 60px;

  border: none;

  border-radius: 40px;

  background: linear-gradient(
    135deg,
    #e6493d,
    #ee9b5c
  );

  color: white;

  font-size: 20px;
  font-weight: 700;

  cursor: pointer;
}

/* EMPTY */

.empty-state{
  text-align: center;
  margin-top: 80px;
}

.empty-state h2{
  font-size: 42px;
  margin-bottom: 10px;
}

.empty-state p{
  font-size: 18px;
  color: #777;
}

/* SORT */

.sort-tabs{
  display: flex;
  justify-content: center;
  gap: 15px;

  margin-bottom: 35px;
}

.tab-btn{
  border: none;

  padding: 12px 24px;

  border-radius: 30px;

  background: #ececec;

  cursor: pointer;

  font-size: 16px;
  font-weight: 600;
}

.tab-btn.active{
  background: linear-gradient(
    135deg,
    #e86b56,
    #f09b5f
  );

  color: white;
}

/* PROFILES */

.profiles-grid{
  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(300px, 1fr));

  gap: 25px;
}

.profile-card{
  position: relative;

  height: 430px;

  overflow: hidden;

  border-radius: 20px;

  background: white;

  box-shadow: 0 6px 20px rgba(0,0,0,0.1);

  transition: 0.3s;
}

.profile-card:hover{
  transform: translateY(-5px);
}

.profile-img{
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* MATCH */

.match-tag{
  position: absolute;

  top: 15px;
  left: 15px;

  z-index: 5;

  background: linear-gradient(
    135deg,
    #e86b56,
    #f09b5f
  );

  color: white;

  padding: 8px 14px;

  border-radius: 10px;

  font-size: 14px;
  font-weight: 700;
}

/* OVERLAY */

.profile-overlay{
  position: absolute;

  bottom: 0;
  left: 0;

  width: 100%;

  padding: 25px 20px;

  background: linear-gradient(
    to top,
    rgba(0,0,0,0.75),
    rgba(0,0,0,0)
  );

  color: white;
}

.profile-overlay h3{
  font-size: 34px;
  margin-bottom: 5px;
}

.location-text{
  font-size: 16px;
}

/* SAVE */

.save-btn{
  position: absolute;

  top: 15px;
  right: 15px;

  border: none;

  background: rgba(255,255,255,0.9);

  padding: 10px 14px;

  border-radius: 10px;

  cursor: pointer;

  font-weight: 600;
}

/* MOBILE */

@media (max-width: 768px){

  .search-header h1{
    font-size: 36px;
  }

  .filter-overlay{
    right: 0;
    left: 0;

    display: flex;
    justify-content: center;
  }

  .filter-modal{
    width: 92%;
  }

  .profiles-grid{
    grid-template-columns: 1fr;
  }
}

</style>