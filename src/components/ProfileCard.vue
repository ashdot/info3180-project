<template>
  <div v-if="profile" class="profile-card">

    <!-- PHOTO -->
    <div class="image-container">
      <img
        v-if="profile.photo || profile.photo_url"
        :src="profile.photo || profile.photo_url"
        :alt="profile.first_name"
        class="profile-img"
      />
      <div v-else class="avatar-placeholder">
        {{ profile.first_name?.charAt(0)?.toUpperCase() }}
      </div>
    </div>

    <!-- BODY -->
    <div class="card-body">

      <div class="card-header">
        <h3>{{ profile.first_name }} {{ profile.last_name }}<span class="age">, {{ profile.age }}</span></h3>
        <p v-if="profile.location" class="location">{{ profile.location }}</p>
      </div>

      <p v-if="profile.bio" class="bio">{{ profile.bio }}</p>

      <div v-if="profile.education" class="education">
        <span>🎓</span>
        <span>{{ profile.education }}</span>
      </div>

      <div v-if="interestList.length" class="tags">
        <span v-for="interest in interestList" :key="interest" class="interest-tag">
          {{ interest }}
        </span>
      </div>

      <!-- ACTIONS -->
      <div class="card-actions">
        <slot name="actions">
          <button class="action-btn dislike" @click="$emit('dislike', profile.user_id)" title="Dislike">✕</button>
          <button class="action-btn like"    @click="$emit('like',    profile.user_id)" title="Like">♥</button>
        </slot>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  profile: { type: Object, required: true }
})

defineEmits(['like', 'dislike', 'save'])

const interestList = computed(() => {
  if (!props.profile?.interests) return []
  try {
    const parsed = JSON.parse(props.profile.interests)
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return props.profile.interests.split(',').map(i => i.trim()).filter(Boolean)
  }
})
</script>

<style scoped>
.profile-card {
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
  background: white;
  box-shadow: 0 6px 20px rgba(0,0,0,0.10);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.profile-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0,0,0,0.14);
}

/* PHOTO */
.image-container {
  width: 100%;
  height: 220px;
  flex-shrink: 0;
  overflow: hidden;
}

.profile-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top;
  display: block;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #ff4d4d, #ff7a45);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 64px;
  font-weight: 700;
}

/* BODY */
.card-body {
  padding: 16px 18px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.card-header { }

.card-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: #111;
  margin-bottom: 2px;
}

.age {
  font-weight: 400;
  color: #666;
}

.location {
  font-size: 13px;
  color: #888;
}

.bio {
  font-size: 13px;
  color: #555;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.education {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #666;
}

/* TAGS */
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.interest-tag {
  background: #fff0e5;
  color: #e86b56;
  border-radius: 999px;
  padding: 3px 12px;
  font-size: 12px;
  font-weight: 500;
  border: 1px solid #e86b56;
}

/* ACTIONS */
.card-actions {
  display: flex;
  justify-content: center;
  gap: 14px;
  padding-top: 8px;
  border-top: 1px solid #f0f0f0;
  margin-top: auto;
}

.action-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 2px solid #eee;
  background: white;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.action-btn:hover      { transform: scale(1.1); }
.action-btn.like       { border-color: #ff4d4d; color: #ff4d4d; }
.action-btn.like:hover { background: #ff4d4d; color: white; }
.action-btn.dislike       { border-color: #ccc; color: #999; }
.action-btn.dislike:hover { background: #f3f4f6; }
.action-btn.save          { border-color: #ff7a45; color: #ff7a45; }
.action-btn.save:hover    { background: #ff7a45; color: white; }
.action-btn.message       { border-color: #6366f1; color: #6366f1; }
.action-btn.message:hover { background: #6366f1; color: white; }
</style>