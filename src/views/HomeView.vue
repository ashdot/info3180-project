<template>
  <div>

    <!-- LANDING -->
    <section class="landing">
      <div class="content">
        <h1>Find Your Perfect <span>Match</span></h1>
        <p>
          Connect with compatible singles in Jamaica. Create your profile,
          discover matches, and start meaningful conversations today!
        </p>
        <button class="cta-hero" @click="$router.push('/signup')">
          Get Started
        </button>
      </div>
    </section>

    <!-- FEATURES -->
    <section class="features">
      <h2>Why Choose DriftDater?</h2>
      <p class="features-sub">Everything you need to find your perfect match</p>

      <div class="grid">
        <FeatureCard
          :icon="iconMatching"
          title="Smart Matching"
          text="Our algorithm finds compatible matches based on your interests, location, and preferences."
        />
        <FeatureCard
          :icon="iconSecure"
          title="Safe & Secure"
          text="Your privacy is our priority. All profiles are verified and your data is protected."
        />
        <FeatureCard
          :icon="iconMessaging"
          title="Easy Messaging"
          text="Chat with your matches instantly. Start meaningful conversations with ease."
        />
        <FeatureCard
          :icon="iconConnections"
          title="Real Connections"
          text="Join thousands of singles looking for genuine relationships and connection."
        />
      </div>
    </section>

    <!-- CTA -->
    <section class="cta">
      <h2>Ready to Find Love?</h2>
      <p>Join DriftDater today and start your journey</p>
      <button @click="$router.push('/signup')">
        Create Your Profile Now
      </button>
    </section>

  </div>
</template>

<script setup>
import FeatureCard from '@/components/FeatureCard.vue'

const iconMatching = `<svg width="41px" height="41px" viewBox="0 0 24 24" stroke-width="1.5" fill="none" xmlns="http://www.w3.org/2000/svg" color="#ffffff"><path d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path><path d="M13 6.5C16.1338 6.5 17.5 5.18153 17.5 2C17.5 5.18153 18.8567 6.5 22 6.5C18.8567 6.5 17.5 7.85669 17.5 11C17.5 7.85669 16.1338 6.5 13 6.5Z" stroke="#ffffff" stroke-width="1.5" stroke-linejoin="round"></path></svg>`
const iconSecure = `<svg width="41px" height="41px" stroke-width="1.5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" color="#ffffff"><path d="M8.5 11.5L11.5 14.5L16.5 9.5" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path><path d="M5 18L3.13036 4.91253C3.05646 4.39524 3.39389 3.91247 3.90398 3.79912L11.5661 2.09641C11.8519 2.03291 12.1481 2.03291 12.4339 2.09641L20.096 3.79912C20.6061 3.91247 20.9435 4.39524 20.8696 4.91252L19 18C18.9293 18.495 18.5 21.5 12 21.5C5.5 21.5 5.07071 18.495 5 18Z" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg>`
const iconMessaging = `<svg width="41px" height="41px" stroke-width="1.5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" color="#ffffff"><path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 13.8214 2.48697 15.5291 3.33782 17L2.5 21.5L7 20.6622C8.47087 21.513 10.1786 22 12 22Z" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg>`
const iconConnections = `<svg width="41px" height="41px" stroke-width="1.5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" color="#ffffff"><path d="M22 8.86222C22 10.4087 21.4062 11.8941 20.3458 12.9929C17.9049 15.523 15.5374 18.1613 13.0053 20.5997C12.4249 21.1505 11.5042 21.1304 10.9488 20.5547L3.65376 12.9929C1.44875 10.7072 1.44875 7.01723 3.65376 4.73157C5.88044 2.42345 9.50794 2.42345 11.7346 4.73157L11.9998 5.00642L12.2648 4.73173C13.3324 3.6245 14.7864 3 16.3053 3C17.8242 3 19.2781 3.62444 20.3458 4.73157C21.4063 5.83045 22 7.31577 22 8.86222Z" stroke="#ffffff" stroke-width="1.5" stroke-linejoin="round"></path></svg>`

</script>

<style scoped>
/* LANDING */
.landing {
  min-height: 560px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 40px 20px;
  background:
    linear-gradient(
      to bottom,
      rgba(255,77,77,0) 0%,
      rgba(255,122,69,0.6) 75%,
      rgba(255,77,77,0.88) 100%
    ),
    url('@/assets/landing.jpg') center/cover no-repeat;
}

.content {
  max-width: 700px;
}

.landing h1 {
  font-size: clamp(36px, 7vw, 80px);
  color: white;
  font-weight: 800;
  line-height: 1.05;
  margin-bottom: 20px;
  text-shadow: 0 2px 12px rgba(0,0,0,0.2);
}

.landing span {
  color: #ff3b30;
}

.landing p {
  color: rgba(255,255,255,0.92);
  max-width: 560px;
  line-height: 1.6;
  font-size: 17px;
  margin: 0 auto 28px;
}

.cta-hero {
  background: white;
  color: #ff4d4d;
  padding: 14px 36px;
  border-radius: 30px;
  border: none;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  transition: transform 0.2s, box-shadow 0.2s;
}

.cta-hero:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(0,0,0,0.2);
}

/* FEATURES */
.features {
  padding: 80px 40px;
  text-align: center;
  background: #f9f9fb;
}

.features h2 {
  font-size: 32px;
  font-weight: 800;
  color: #111;
  margin-bottom: 8px;
}

.features-sub {
  color: #aaa;
  font-size: 16px;
  margin-bottom: 48px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(280px, 360px));
  justify-content: center;
  gap: 40px 80px;
}

/* CTA */
.cta {
  background: linear-gradient(135deg, #ff4d4d, #ff7a45);
  text-align: center;
  padding: 80px 40px;
  color: white;
}

.cta h2 {
  font-size: 32px;
  font-weight: 800;
  margin-bottom: 10px;
}

.cta p {
  font-size: 16px;
  opacity: 0.9;
  margin-bottom: 28px;
}

.cta button {
  background: white;
  color: #ff4d4d;
  padding: 14px 36px;
  border-radius: 30px;
  border: none;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  transition: transform 0.2s, box-shadow 0.2s;
}

.cta button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(0,0,0,0.2);
}

/* MOBILE */
@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
    gap: 30px;
    padding: 0 20px;
  }

  .landing h1 { font-size: 38px; }

  .landing p {
    font-size: 15px;
    padding: 0 10px;
  }

  .features { padding: 60px 20px; }
  .cta { padding: 60px 20px; }
}
</style>