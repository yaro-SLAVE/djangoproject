<script setup lang="ts">
    import {computed, ref, onBeforeMount} from 'vue';
    import axios from "axios";
    import Cookies from 'js-cookie';

    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchData();
    })

    async function fetchData() {
        const r = await axios.get("/api/users/");
        const d = await axios.get("/api/roles/");
        const g = await axios.get("/api/groups/");
        const p = await axios.get("/api/profiles/");
        profiles.value = p.data;
        users.value = r.data;
        roles.value = d.data;   
        groups.value = g.data;
    }

    const groups = ref([]);
    const profiles = ref([]);
    const profileToAdd = ref({});
    const roles = ref({});
    const users = ref({});

    async function onLoadClick() {
        const r = await axios.get("/api/profiles/");
        console.log(r.data);
        profiles.value = r.data;
    }

    async function onProfileAdd() {
        await axios.post("/api/profiles/", {
            ...profileToAdd.value,
        });
        await fetchData();
    }
</script>

<template>
    <div>
        <div v-for="item in profiles">
            <b>{{ item.user.username }}</b>
        </div>

        <button @click="onLoadClick">Загрузить</button>
    </div>

    <form @submit.prevent.stop="onProfileAdd">
        <div class="row">
            <div class="col">
                <div class="form-floating">
                    <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
                    <input
                    type="text"
                    class="form-control"
                    v-model="profileToAdd.profile_name"
                    required
                    />
                    <label for="floatingInput">Фио</label>
                </div>
            </div>
            <div class="col-auto">
                <!-- А ТУТ ПОДКЛЮЧИЛ К select -->
                <div class="form-floating">
                    <select class="form-select" v-model="profileToAdd.group_id" required>
                        <option :value="g.id" v-for="g in groups">{{ g.group_name }}</option>
                    </select>
                    <label for="floatingInput">Группа</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-select" v-model="profileToAdd.role_id" required>
                        <option :value="g.id" v-for="g in roles">{{ g.role }}</option>
                    </select>
                    <label for="floatingInput">Роль</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-select" v-model="profileToAdd.user_id" required>
                        <option :value="g.id" v-for="g in users">{{ g.username }}</option>
                    </select>
                    <label for="floatingInput">User</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
                    <input
                    type="number"
                    class="form-control"
                    v-model="profileToAdd.total_scores"
                    required
                    />
                    <label for="floatingInput">баллы</label>
                </div>
            </div>
            <div class="col-auto">
                <button class="btn btn-primary">
                    Добавить
                </button>
            </div>
        </div>
    </form>
</template>

<style scoped>
</style>
