<template>
  <div class="page">

    <div class="card">

      <!-- HEADER -->
      <div class="header">

        <div class="profile-photo-section" @click="triggerFile">

          <input
            type="file"
            ref="fileInput"
            hidden
            accept="image/*"
            @change="handleFile"
          />

          <div class="profile-photo">

            <img
              v-if="preview"
              :src="preview"
              alt="Profile"
            />

            <span v-else>Upload</span>

          </div>

          <p>Change Profile Photo</p>

        </div>

      </div>

      <h1>Edit Profile</h1>

      <p class="subtitle">
        Update your personal information
      </p>

      <!-- FORM -->
      <form @submit.prevent="saveProfile">

        <!-- NAME + AGE -->
        <div class="row">

          <div class="field">
            <label>Full Name</label>

            <input
              type="text"
              v-model="name"
              placeholder="John Doe"
            />
          </div>

          <div class="field">
            <label>Age</label>

            <input
              type="number"
              v-model="age"
              placeholder="25"
            />
          </div>

        </div>

        <!-- EMAIL -->
        <div class="field">
          <label>Email</label>

          <input
            type="email"
            v-model="email"
            placeholder="john@email.com"
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

          <input
            type="text"
            v-model="interests"
            placeholder="Music, Movies, Travel"
          />
        </div>

        <!-- GENDER + LOOKING FOR -->
        <div class="row">

          <div class="field">
            <label>Gender</label>

            <select v-model="gender">
              <option>Male</option>
              <option>Female</option>
            </select>
          </div>

          <div class="field">
            <label>Looking For</label>

            <select v-model="lookingFor">
              <option>Male</option>
              <option>Female</option>
            </select>
          </div>

        </div>

        <!-- VISIBILITY -->
        <div class="field">
          <label>Profile Visibility</label>

          <select v-model="visibility">
            <option>Public</option>
            <option>Private</option>
          </select>
        </div>

        <!-- BUTTONS -->
        <div class="button-group">

          <button
            type="button"
            class="cancel-btn"
            @click="$router.push('/profile')"
          >
            Cancel
          </button>

          <button class="save-btn">
            Save Changes
          </button>

        </div>

      </form>

    </div>

  </div>
</template>

<script>
export default {

  data() {
    return {

      name: "John Doe",
      age: 25,
      email: "john@example.com",
      location: "Kingston, Jamaica",

      bio: "Love music, food and travelling.",
      interests: "Movies, Music, Sports",

      gender: "Male",
      lookingFor: "Female",

      visibility: "Public",

      preview: null
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

      const updatedUser = {
        name: this.name,
        age: this.age,
        email: this.email,
        location: this.location,
        bio: this.bio,
        interests: this.interests,
        gender: this.gender,
        lookingFor: this.lookingFor,
        visibility: this.visibility,
        profilePhoto: this.preview
      };

      console.log(updatedUser);

      alert("Profile Updated Successfully!");

      this.$router.push('/profile');
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
  background: white;
  padding: 35px;
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}

.header {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.profile-photo-section {
  text-align: center;
  cursor: pointer;
}

.profile-photo {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  background: #eee;
  border: 4px solid #ffd6e0;

  display: flex;
  justify-content: center;
  align-items: center;

  overflow: hidden;

  margin: auto;
}

.profile-photo span {
  color: #888;
  font-size: 14px;
}

.profile-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-photo-section p {
  margin-top: 10px;
  color: #ff4d79;
  font-weight: 600;
}

h1 {
  text-align: center;
  margin-bottom: 8px;
}

.subtitle {
  text-align: center;
  color: gray;
  margin-bottom: 25px;
}

.row {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.field {
  flex: 1;
  margin-top: 15px;
}

.field label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

input,
select,
textarea {
  width: 100%;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid #ddd;
  font-size: 14px;
  box-sizing: border-box;
  transition: 0.2s ease;
}

textarea {
  min-height: 110px;
  resize: none;
  font-family: inherit;
}

input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #ff4d79;
  box-shadow: 0 0 0 3px rgba(255, 77, 121, 0.1);
}

.button-group {
  display: flex;
  gap: 15px;
  margin-top: 30px;
}

.cancel-btn,
.save-btn {
  flex: 1;
  padding: 14px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  font-weight: bold;
  font-size: 15px;
  transition: 0.2s ease;
}

.cancel-btn {
  background: #eee;
  color: #333;
}

.cancel-btn:hover {
  background: #ddd;
}

.save-btn {
  background: linear-gradient(135deg, #ff4d79, #ff6a5c);
  color: white;
}

.save-btn:hover {
  transform: translateY(-2px);
  opacity: 0.95;
}

/* MOBILE */
@media (max-width: 700px) {

  .row {
    flex-direction: column;
    gap: 0;
  }

  .button-group {
    flex-direction: column;
  }

  .card {
    padding: 25px;
  }
}

</style>