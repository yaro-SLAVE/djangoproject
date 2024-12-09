<script setup lang="ts">
    import {computed, ref, onBeforeMount, onActivated, onMounted} from 'vue';
    import { storeToRefs } from 'pinia';
    import useUserProfileStore from '../stores/userProfileStore';
    import type { User } from '@/customTypes';
    import axios from 'axios';

    const userProfileStore = useUserProfileStore();

    const {
        userProf,
        jwt
    } = storeToRefs(userProfileStore);

    const logo = ref();
    const logoURL = ref();

    onBeforeMount(async () => {
        
    });

    async function changeLogo() {
        logoURL.value = URL.createObjectURL(logo.value.files[0]);
    }
    
    async function updateInfo() {
        const user = (await axios.get("/api/user/user_id/", {
            headers: {
                Authorization: `Bearer ${jwt.value}`
            }
        })).data;

        const profData = new FormData();
        profData.append('first_name', String(userProf.value?.first_name));
        profData.append('last_name', String(userProf.value?.last_name));
        profData.append('email', String(userProf.value?.email));

        const prof = await axios.put("/api/user/" + user.id + "/", profData, {
            headers: {
                Authorization: `Bearer ${jwt.value}`
            }
        });
    }

    async function updateLogo() {
        if (logo.value.files[0] !== undefined) {
            const formData = new FormData();
        
            formData.append('image', logo.value.files[0]);

            const logoData = await axios.post("/api/image/", formData, {
                headers: {
                    Authorization: `Bearer ${jwt.value}`
                }
            });

            const user = (await axios.get("/api/profile/profile_id/", {
                headers: {
                    Authorization: `Bearer ${jwt.value}`
                }
            })).data;

            const profLogoData = new FormData();
            profLogoData.append('profile_logo', logoData.data.id);

            const prof = await axios.put("/api/profile/" + user.id + "/", profLogoData, {
                headers: {
                    Authorization: `Bearer ${jwt.value}`
                }
            });

            await userProfileStore.getUserInfo();

            logo.value = "";
            logoURL.value = "";
        }
    }
</script>

<template>
    <div class="row mt-5 align-items-center">
        <div class="col-6 text-center d-flex flex-column">
            <label class="mb-4">{{userProf?.username}}</label>

            <div class="profile-image-wrap-block">
                <img v-if="userProf?.logo === undefined" src="../../default_profile.jpg" class="img-fluid" style="height: 100%">
                <img v-if="userProf?.logo !== undefined" :src='userProf?.logo' class="img-fluid" style="height: 100%">
            </div>

            <button id="addTask" type="button" class="btn btn-primary my-4" data-bs-toggle="modal" data-bs-target="#changeLogoModal">Изменить фото</button>
        </div>

        <div class="col-6 text-start px-5">
            <p>{{userProf?.last_name + " " + userProf?.first_name}}</p>
            <p>Роль: {{userProf?.role_description}}</p>
            <p v-if="userProf?.role === 'student'">Группа: {{userProf?.group}}</p>
            <p>E-mail: {{userProf?.email}}</p>
            <p>Количество очков: {{userProf?.total_scores}}</p>
            <button id="addTask" type="button" class="btn btn-primary my-4" data-bs-toggle="modal" data-bs-target="#changeInfoModal">Исправить инфу</button>
        </div>
    </div>

    <div class="modal fade" id="changeLogoModal" tabindex="-1" aria-labelledby="logoModal" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="logoModalLabel">Изменение фото Профиля</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form class="d-flex flex-column justify-content-center mb-4 text-center" @submit.prevent.stop="updateLogo">
                        <label class="form-label" for="login">Выберите фото профиля</label>
                        
                        <input type="file" class="form-control" ref="logo" @change="changeLogo()"/>

                        <div class="profile-small-image-wrap-block my-4 text-center">
                            <img :src="logoURL" class="img-fluid" style="height: 100%">
                        </div>
                                            
                        <button class="btn btn-primary" data-bs-dismiss="modal">Сохранить фото</button>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" id="changeInfoModal" tabindex="-1" aria-labelledby="changeModal" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="addTaskModalLabel">Изменение данных Профиля</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form class="d-flex flex-column justify-content-center mb-4" @submit.prevent.stop="updateInfo">
                        <div data-mdb-input-init class="form-outline mb-4">
                            <label class="form-label">Имя</label>
                            <input type="text" class="form-control" v-model="userProf.first_name" required/>
                        </div>

                        <div data-mdb-input-init class="form-outline mb-4">
                            <label class="form-label">Фамилия</label>
                            <input type="text" class="form-control"  v-model="userProf.last_name" required/>
                        </div>

                        <div data-mdb-input-init class="form-outline mb-4">
                            <label class="form-label">E-mail</label>
                            <input type="email" class="form-control"  v-model="userProf.email"/>
                        </div>
                                            
                        <button class="btn btn-primary btn-block mb-4">Сохранить изменения</button>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .profile-image-wrap-block {
        width: 300px; 
        height: 300px; 
        border-radius: 50%;
        overflow: hidden;
    }

    .profile-small-image-wrap-block {
        width: 120px; 
        height: 120px; 
        border-radius: 50%;
        overflow: hidden;
    }
</style>