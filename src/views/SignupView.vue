<template>
  <div class="page">
    <div class="card">

      <!-- LOGO -->
      <div class="logo">
        <img src="@/assets/logo.png" alt="DriftDater Logo" />
      </div>

      <h1>Create Your Profile</h1>
      <p class="subtitle">
        Join thousands of singles looking for love
      </p>

      <!-- PROFILE PHOTO -->
      <div class="upload-box" @click="triggerFile">
        <input
          type="file"
          ref="fileInput"
          hidden
          accept="image/*"
          @change="handleFile"
        />

        <div class="upload-circle">
          <img v-if="preview" :src="preview" />
          <span v-else>Upload</span>
        </div>

        <p class="upload-text">Upload Profile Photo</p>
      </div>

      <!-- FORM -->
      <form @submit.prevent="handleSignup">

        <!-- NAME + AGE -->
        <div class="row">

          <div class="field">
            <label>Full Name *</label>
            <input
              type="text"
              placeholder="John Doe"
              v-model="name"
            />
          </div>

          <div class="field">
            <label>Age *</label>
            <input
              type="number"
              placeholder="25"
              v-model="age"
            />
          </div>

        </div>

        <!-- EMAIL -->
        <div class="field">
          <label>Email *</label>
          <input
            type="email"
            placeholder="you@example.com"
            v-model="email"
          />
        </div>

        <!-- LOCATION -->
        <div class="field">
          <label>Location *</label>
          <input
            type="text"
            placeholder="Kingston, Jamaica"
            v-model="location"
          />
        </div>

        <!-- BIO -->
        <div class="field">
          <label>Bio</label>
          <textarea
            placeholder="Tell others about yourself..."
            v-model="bio"
          ></textarea>
        </div>

        <!-- INTERESTS -->
        <div class="field">
          <label>Interests</label>
          <input
            type="text"
            placeholder="Music, Movies, Travel"
            v-model="interests"
          />
        </div>

        <!-- VISIBILITY -->
        <div class="field">
          <label>Profile Visibility</label>
          <select v-model="visibility">
            <option>Public</option>
            <option>Private</option>
          </select>
        </div>

        <!-- GENDER -->
        <div class="row">

          <div class="field">
            <label>Gender *</label>
            <select v-model="gender">
              <option disabled value="">Select gender</option>
              <option>Male</option>
              <option>Female</option>
            </select>
          </div>

          <div class="field">
            <label>Looking For *</label>
            <select v-model="lookingFor">
              <option disabled value="">Select preference</option>
              <option>Male</option>
              <option>Female</option>
            </select>
          </div>

        </div>

        <!-- PASSWORDS -->
        <div class="row">

          <div class="field">
            <label>Password *</label>

            <div class="input-box">
              <input
                :type="showPassword ? 'text' : 'password'"
                placeholder="Enter password"
                v-model="password"
              />

              <button
                type="button"
                class="toggle"
                @click="showPassword = !showPassword"
              >
                {{ showPassword ? 'Hide' : 'Show' }}
              </button>
            </div>
          </div>

          <div class="field">
            <label>Confirm Password *</label>

            <div class="input-box">
              <input
                :type="showConfirm ? 'text' : 'password'"
                placeholder="Confirm password"
                v-model="confirmPassword"
              />

              <button
                type="button"
                class="toggle"
                @click="showConfirm = !showConfirm"
              >
                {{ showConfirm ? 'Hide' : 'Show' }}
              </button>
            </div>
          </div>

        </div>

        <!-- TERMS -->
        <div class="terms">

          <input
            type="checkbox"
            v-model="agree"
          />

          <p>
            I agree to the
            <span>Terms of Service</span>
            and
            <span>Privacy Policy</span>.
          </p>

        </div>

        <!-- BUTTON -->
        <button class="btn">
          Create Account
        </button>

      </form>

      <!-- LOGIN -->
      <p class="bottom">
        Already have an account?

        <span @click="$router.push('/login')">
          Login
        </span>
      </p>

    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {

      name: "",
      age: "",
      email: "",
      location: "",

      bio: "",
      interests: "",
      visibility: "Public",

      gender: "",
      lookingFor: "",

      password: "",
      confirmPassword: "",

      agree: false,

      preview: null,

      showPassword: false,
      showConfirm: false
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

    handleSignup() {

      if (
        !this.name ||
        !this.age ||
        !this.email ||
        !this.location ||
        !this.gender ||
        !this.lookingFor ||
        !this.password ||
        !this.confirmPassword
      ) {
        alert("Please fill in all required fields");
        return;
      }

      if (this.password !== this.confirmPassword) {
        alert("Passwords do not match");
        return;
      }

      if (!this.agree) {
        alert("Please agree to the Terms and Conditions");
        return;
      }

      const userData = {
        name: this.name,
        age: this.age,
        email: this.email,
        location: this.location,
        bio: this.bio,
        interests: this.interests,
        visibility: this.visibility,
        gender: this.gender,
        lookingFor: this.lookingFor,
        profilePhoto: this.preview
      };

      console.log(userData);

      alert("Account Created Successfully!");

      this.$router.push("/login");
    }
  }
};
</script>

<style scoped>

.page {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
  min-height: 100vh;
  background: #f5f5f7;
}

.card {
  width: 100%;
  max-width: 600px;
  background: white;
  padding: 35px;
  border-radius: 18px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
  text-align: center;
}

.logo {
  margin-bottom: 10px;
}

.logo img {
  width: 75px;
  height: 75px;
  object-fit: contain;
}

h1 {
  margin-bottom: 8px;
  color: #222;
}

.subtitle {
  color: gray;
  margin-bottom: 25px;
}

.upload-box {
  cursor: pointer;
  margin-bottom: 20px;
}

.upload-circle {
  width: 95px;
  height: 95px;
  border-radius: 50%;
  background: #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: auto;
  overflow: hidden;
  border: 3px solid #ffd6e0;
}

.upload-circle span {
  color: #999;
  font-size: 14px;
}

.upload-circle img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-text {
  margin-top: 10px;
  color: #ff4d79;
  font-weight: 500;
}

.row {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.field {
  flex: 1;
  text-align: left;
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
  transition: 0.2s ease;
  box-sizing: border-box;
}

textarea {
  min-height: 100px;
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

input::placeholder,
textarea::placeholder {
  color: #aaa;
}

/* REMOVE EDGE PASSWORD ICON */
input[type="password"]::-ms-reveal,
input[type="password"]::-ms-clear {
  display: none;
}

/* PASSWORD INPUT */
.input-box {
  position: relative;
}

.input-box input {
  padding-right: 70px;
}

.toggle {
  position: absolute;
  right: 10px;
  top: 11px;
  background: none;
  border: none;
  color: #ff4d79;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
}

/* TERMS */
.terms {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-top: 20px;
  text-align: left;
}

.terms input {
  width: auto;
  margin-top: 4px;
}

.terms p {
  margin: 0;
  font-size: 14px;
  color: #555;
  line-height: 1.5;
}

.terms span {
  color: #ff4d79;
  font-weight: 600;
  cursor: pointer;
}

/* BUTTON */
.btn {
  width: 100%;
  margin-top: 25px;
  padding: 14px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, #ff4d79, #ff6a5c);
  color: white;
  font-size: 15px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.2s ease;
}

.btn:hover {
  transform: translateY(-2px);
  opacity: 0.95;
}

/* LOGIN */
.bottom {
  margin-top: 20px;
  color: #666;
}

.bottom span {
  color: #ff4d79;
  cursor: pointer;
  font-weight: 600;
}

/* MOBILE */
@media (max-width: 700px) {

  .row {
    flex-direction: column;
    gap: 0;
  }

  .card {
    padding: 25px;
  }
}
</style>