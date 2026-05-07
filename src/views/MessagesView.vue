<template>
    <div class="layout">
        
        <Sidebar />

        <main class="page-content">
            
            <div class="heading">
                <h2>Messages</h2>
                <!--<i class="fi fi-br-search"></i>-->
            </div>

            <div
                v-for="contact in contacts"
                :key="contact.username"
                class="conversation"
            >
                <img
                    :src="contact.photo"
                    class="avatar"
                />

                <div class="conversation-info">
                    <h2>
                        {{ contact.first_name }}
                        {{ contact.last_name }}
                    </h2>
                    <!--make it "preview" most recent message-->
                    <!--implement badge to show that theres a ew message-->
                </div>
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

import api from '@/services/api'
import Sidebar from '@/components/Sidebar.vue'

const contacts = ref([])

const userId = localStorage.getItem('user_id')

onMounted(async () => {

    try {

        const response = await api.get(
            `/contacts/${userId}`
        )

        contacts.value = response.data.contacts

    } catch (error) {
        console.error(error)
    }
})
</script>

<style scoped>

.layout {
    display: flex;
    min-height: 100vh;
}

.page-content {
    flex: 1;
    padding: 40px 60px;
    max-width: 1200px;
    margin: 0 auto;
}

.heading {
    display: flex;
    align-items: center;
    justify-content: center; 
    margin-top: 20px;
    margin-bottom: 40px;
}


.conversation {
    display: flex;
    align-items: center;

    gap: 18px;

    padding: 22px 0;

    border-bottom: 1px solid #eee;
}

.avatar {
    width: 72px;
    height: 72px;

    border-radius: 50%;
    object-fit: cover;
}

.conversation-info h2 {
    font-size: 24px;
    margin-bottom: 6px;
}

</style>

