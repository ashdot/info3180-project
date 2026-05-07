<template>
    <div class="layout">
  
        <Sidebar />
  
        <main class="page-content">
  
            <div class="heading">
                <h2>Saved Profiles</h2>
            </div>
  
  
            <div class="favourites-grid">
                <!--edit this
                <div
                    v-for="match in filteredMatches"
                    :key="match.id"
                    class="match-card"
                >
        
                    <img
                        :src="match.photo"
                        class="match-img"
                    />

                    <div class="overlay">

                        <div class="match-percent">
                            {{ Math.round(match.score * 20) }}% Match
                        </div>

                        <div class="match-info">
                            <h2>
                                {{ match.first_name }}
                            </h2>
                            
                            <div class="location-row">

                            </div>
                        </div>
                    </div>
                </div>  --> 
            </div>
        </main>
    </div>
</template>
  
<script setup>
import { ref, computed, onMounted } from 'vue'
  
import api from '@/services/api'
import Sidebar from '@/components/Sidebar.vue'

</script>
  
<style scoped>
 
.layout {
    display: flex;
    min-height: 100vh;
}

.sidebar {
    width: 260px;
    flex-shrink: 0;
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
    margin-bottom: 10px;
}
  
.favourites-grid {
    display: grid;
  
    grid-template-columns:
      repeat(auto-fill, minmax(260px, 1fr));
  
    gap: 28px;
}
 
/*
.match-card {
    position: relative;
  
    height: 380px;
  
    border-radius: 18px;
    overflow: hidden;
  
    cursor: pointer;
}
  
.match-img {
    width: 100%;
    height: 100%;
  
    object-fit: cover;
}
  
.overlay {
    position: absolute;
    inset: 0;
  
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
  
    padding: 18px;
  
    background: linear-gradient(
      to top,
      rgba(0,0,0,0.72),
      transparent 60%
    );
}
  
.match-percent {
    position: absolute;
    top: 14px;
    left: 14px;
  
    background: linear-gradient(
      to right,
      #ff4d4d,
      #ff7a45
    );
  
    color: white;
  
    padding: 8px 12px;
    border-radius: 10px;
  
    font-weight: 700;
}
  
.match-info h2 {
    color: white;
    font-size: 32px;
    margin-bottom: 6px;
}
 
/*
.location-row {
    display: flex;
    align-items: center;
    gap: 6px;
}
  
.location-row p {
    color: white;
}
  
.location-icon {
    width: 14px;
    height: 14px;
}*/
</style>