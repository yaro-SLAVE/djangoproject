<script setup lang="ts">
    import {computed, ref, onBeforeMount} from 'vue';
    import axios from "axios";
    import Cookies from 'js-cookie';

    interface User {
        username: string;
    }

    interface Role {
        role: string;
    }

    interface Group {
        group: string;
    }

    interface Profile {
        user: User;
        role: Role;
        group: Group;
        total_scores: number;
    }

    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchData();
    })

    async function fetchData() {
        const p = await axios.get("/api/profiles/");
        console.log(p.data)
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
          <a class="navbar-brand" href="#">Navbar</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Профиль
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                        <li><a class="dropdown-item" href="/admin">Админка</a></li>
                    </ul>
                </li>
            </ul>
            </div>
        </div>
    </nav>
</template>

<style scoped>
</style>
