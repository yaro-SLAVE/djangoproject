<script setup lang="ts">
    import {computed, ref, onBeforeMount, onActivated, onMounted} from 'vue';
    import axios from "axios";
    import Cookies from 'js-cookie';
    import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
    import { faBookmark }  from '@fortawesome/free-regular-svg-icons'
    import { storeToRefs } from 'pinia';
    import useUserProfileStore from './stores/userProfileStore';
    import router from './router/index'

    interface Role {
        role: string;
    }

    interface Group {
        group: string;
    }

    interface Profile {
        role: Role;
        group: Group;
        total_scores: number;
    }

    const userProfileStore = useUserProfileStore();

    const {
        is_auth,
        is_superuser,
        username
    } = storeToRefs(userProfileStore);

    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

        await fetchData();
    })

    onMounted(() => {
        if ((!is_auth.value && (router.currentRoute.value.path !== '/login')) || (!is_auth.value && (router.currentRoute.value.path !== '/registration'))) {
            router.push('/login');
        }
    })

    async function fetchData() {

    }

    const groups = ref([]);
    const profileToAdd = ref({});
    const roles = ref({});
    const users = ref({});

    async function onProfileAdd() {
        await axios.post("/api/profiles/", {
            ...profileToAdd.value,
        });
        await fetchData();
    }
</script>

<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
          <a class="navbar-brand" href="/">
            <FontAwesomeIcon :icon="faBookmark" />
          </a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0 d-flex flex-row">
                <li class="nav-item">
                    <a class="nav-link" href="/tasks">
                        Задания
                    </a>
                </li>

                <li class="nav-item">
                    <a class="nav-link" href="/tests">
                        Тесты
                    </a>
                </li>

                <li class="nav-item dropdown ml-auto justify-content-end">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Профиль
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                        <li><a class="dropdown-item" href="/profile">Мой Профиль</a></li>
                        <li><a class="dropdown-item" href="/admin">Админка</a></li>
                    </ul>
                </li>
            </ul>
            </div>
        </div>
    </nav>

    <router-view/>
</template>

<style scoped>
</style>
