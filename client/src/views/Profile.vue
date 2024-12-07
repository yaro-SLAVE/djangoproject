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

    const changedInfo = userProf.value;
    const logo = ref();

    onBeforeMount(async () => {

    });
    
    async function changeInfo() {
        const result = await axios.put("/api/profile/", {
            headers: {
                Authorization: `Bearer ${jwt.value}`
            },


        })
    }

    async function updateLogo() {
        const formData = new FormData();
        
        formData.append('image', logo.value.files[0]);

        const logoData = await axios.post("/api/image/", formData, {
            headers: {
                Authorization: `Bearer ${jwt.value}`
            }
        });

        const user = (await axios.get("/api/profile/user_id/", {
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

        userProfileStore.getUserInfo();
    }
</script>

<template>
    <div class="row mt-5 align-items-center">
        <div class="col-6 text-center d-flex flex-column">
            <label class="mb-4">{{userProf?.username}}</label>

            <img v-if="userProf?.logo === undefined" src="../../public/default_profile.jpg" class="img-fluid rounded" style="max-height: 300px; overflow: hiden;">
            <img v-if="userProf?.logo !== undefined" :src='userProf?.logo' class="img-fluid rounded" style="max-height: 300px; overflow: hiden;">

            <button id="addTask" type="button" class="btn btn-primary my-4" data-bs-toggle="modal" data-bs-target="#changeLogoModal">Изменить фото</button>
        </div>

        <div class="col-6 text-center">
            <p>{{userProf?.last_name + " " + userProf?.first_name}}</p>
            <p>Роль: {{userProf?.role_description}}</p>
            <p v-if="userProf?.role === 'student'">Группа: {{userInfo.group}}</p>
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
                    <form class="d-flex flex-column justify-content-center mb-4" @submit.prevent.stop="updateLogo">
                        <label class="form-label" for="login">Выберите фото профиля</label>
                        <input type="file" class="form-control" ref="logo" />
                                            
                        <button class="btn btn-primary btn-block mb-4">Сохранить фото</button>
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
                    <form class="d-flex flex-column justify-content-center mb-4" @submit.prevent.stop="changeInfo">

                                            
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