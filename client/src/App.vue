<script setup lang="ts">
    import {computed, ref, onBeforeMount, onActivated, onMounted} from 'vue';
    import axios from "axios";
    import Cookies from 'js-cookie';
    import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
    import { faBookmark }  from '@fortawesome/free-regular-svg-icons'
    import { storeToRefs } from 'pinia';
    import useUserProfileStore from './stores/userProfileStore';
    import router from "./router/index"

    const userProfileStore = useUserProfileStore();

    const {
        userProf
    } = storeToRefs(userProfileStore);

    const isNotLoginPage = computed({
        get() {
            return router.currentRoute.value.name !== 'Login' && router.currentRoute.value.name !== 'Registration';
        },

        set() {}
    });

    async function logout() {
        await userProfileStore.logout();
    }

    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    });
</script>

<template>
    <nav v-if="isNotLoginPage" class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
          <a class="navbar-brand" href="/">
            <FontAwesomeIcon :icon="faBookmark" />
          </a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav d-flex flex-row">
                <li class="nav-item mx-3" :class="{ 'active': router.currentRoute.value.name === 'Tasks'}">
                    <a class="nav-link" href="/tasks">
                        Задания
                    </a>
                </li>

                <li class="nav-item  mx-3" :class="{ 'active': router.currentRoute.value.name === 'Tests'}">
                    <a class="nav-link" href="/tests">
                        Тесты
                    </a>
                </li>

                <li class="nav-item dropdown mx-3">
                    <a class="nav-link dropdown-toggle form-inline" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <div class="navbar-image-wrap-block">
                            <img v-if="userProf?.logo === undefined" src="../default_profile.jpg" class="img-fluid" style="height: 100%">
                            <img v-if="userProf?.logo !== undefined" :src='userProf?.logo' class="img-fluid" style="height: 100%">
                        </div>
                        <label>{{userProf?.username}}</label>
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                        <li><a class="dropdown-item" href="/profile">Профиль</a></li>
                        <li><a v-if="userProf.role === 'admin'" class="dropdown-item" href="/admin">Админка</a></li>
                        <li><button @click="logout" class="dropdown-item">Выйти</button></li>
                    </ul>
                </li>
            </ul>
            </div>
        </div>
    </nav>

    <main class="container d-flex flex-column justify-content-center align-items-center">
        <router-view/>
    </main>
</template>

<style scoped>
    .navbar-image-wrap-block {
        width: 40px; 
        height: 40px; 
        border-radius: 50%;
        overflow: hidden;
    }

    .profile-image-wrap-block {
        width: 300px; 
        height: 300px; 
        border-radius: 50%;
        overflow: hidden;
    }
</style>
