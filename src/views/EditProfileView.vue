<template>
  <div class="page">

    <Sidebar />
  
    <div class="card">

      <h2>Edit Profile</h2>

      <p class="subtitle">
        Update your profile details
      </p>

      <!-- PHOTO -->
      <div
        class="photo-section"
        @click="triggerFile"
      >

        <input
          type="file"
          ref="fileInput"
          hidden
          accept="image/*"
          @change="handleFile"
        />

        <div class="photo-circle">

          <img
            v-if="preview"
            :src="preview"
          />

          <span v-else>
            Upload
          </span>

        </div>

        <p>Update Profile Photo</p>

      </div>

      <form @submit.prevent="saveProfile">

        <!-- VISIBILITY -->
        <div class="field">

          <label>Visibility</label>

          <select v-model="visibility">

            <option>Public</option>
            <option>Private</option>

          </select>

        </div>

        <!-- PREFERENCE -->
        <div class="field">

          <label>Looking For</label>

          <select v-model="preference">

            <option>Man</option>
            <option>Woman</option>
            <option>Both</option>

          </select>

        </div>

        <!-- EDUCATION -->
        <div class="field">

          <label>Education</label>

          <input
            type="text"
            v-model="education"
            placeholder="University of the West Indies"
          />
        </div>

        <!-- LOCATION -->
        <div class="field">

          <label>Location</label>

          <input
            type="text"
            v-model="location"
            placeholder="Kingston, Jamaica"
          />
        </div>

        <!-- BIO -->
        <div class="field">

          <label>Bio</label>

          <textarea
            v-model="bio"
            placeholder="Tell people about yourself..."
          ></textarea>

        </div>

        <!-- INTERESTS -->
        <div class="field">

          <label>Interests</label>

          <div class="interests-grid">

            <label
              v-for="interest in availableInterests"
              :key="interest"
              class="interest-item"
            >

              <input
                type="checkbox"
                :value="interest"
                v-model="interests"
              />

              {{ interest }}

            </label>

          </div>

        </div>

        <!-- BUTTON -->
        <button class="btn">
          Save Changes
        </button>

      </form>

    </div>

  </div>
</template>

<script>

import Sidebar from '@/components/Sidebar.vue'

export default {
  components: {
    Sidebar
  },

  data() {
    return {

      visibility: "Public",

      preference: "Both",

      education: "",

      interests: [],

      bio: "",

      location: "",

      preview: null,

      availableInterests: [

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
      ]
    };
  },

  methods: {

    triggerFile() {
      this.$refs.fileInput.click();
    },

    handleFile(e) {

      const file = e.target.files[0];

      if (file) {
        this.preview = URL.createObjectURL(file);
      }
    },

    saveProfile() {

      const profileData = {

        visibility: this.visibility,

        preference: this.preference,

        education: this.education,

        interests: this.interests,

        bio: this.bio,

        location: this.location,

        profilePhoto: this.preview
      };

      console.log(profileData);

      alert("Profile Updated!");
    }
  }
};
</script>

<style scoped>

.page {
  min-height: 100vh;

  background: #f5f5f7;

  display: flex;
  justify-content: center;
  align-items: center;

  padding: 40px 20px;
}

.card {
  width: 100%;
  max-width: 650px;

  position: relative;
  z-index: 1;

  background: white;

  padding: 35px;

  border-radius: 20px;

  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}

h2 {
  text-align: center;
  margin-bottom: 10px;
}

.subtitle {
  text-align: center;
  color: gray;
  margin-bottom: 25px;
}

.photo-section {
  text-align: center;
  cursor: pointer;
  margin-bottom: 20px;
}

.photo-circle {
  width: 110px;
  height: 110px;

  border-radius: 50%;

  background: #eee;

  border: 4px solid #ffd6e0;

  margin: auto;

  overflow: hidden;

  display: flex;
  justify-content: center;
  align-items: center;
}

.photo-circle span {
  color: gray;
}

.photo-circle img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-section p {
  margin-top: 10px;
  color: #ff4d79;
  font-weight: 600;
}

.field {
  margin-top: 18px;
}

.field label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
}

input,
select,
textarea {
  width: 100%;

  padding: 12px;

  border-radius: 10px;

  border: 1px solid #ddd;

  box-sizing: border-box;
}

textarea {
  min-height: 120px;
  resize: none;
}

.interests-grid {
  display: grid;

  grid-template-columns: repeat(2, 1fr);

  gap: 10px;

  margin-top: 10px;
}

.interest-item {
  display: flex;
  align-items: center;

  gap: 8px;

  background: #f8f8f8;

  padding: 10px;

  border-radius: 10px;

  cursor: pointer;
}

.interest-item input {
  width: auto;
}

.btn {
  width: 100%;

  margin-top: 30px;

  padding: 14px;

  border: none;
  border-radius: 10px;

  background: linear-gradient(135deg, #ff4d79, #ff6a5c);

  color: white;

  font-weight: bold;

  cursor: pointer;
}

@media (max-width: 700px) {

  .interests-grid {
    grid-template-columns: 1fr;
  }
}
</style>