<script setup lang="ts">
    import {computed, ref, onBeforeMount, onActivated, onMounted} from 'vue';
    import { storeToRefs } from 'pinia';
    import useUserProfileStore from '../stores/userProfileStore';

    const userProfileStore = useUserProfileStore();

    const {
        userProf
    } = storeToRefs(userProfileStore);
</script>

<template>
    <div class="row mt-5 mx-0">
        <div class="col-6">
            <img v-if="userProf?.logo === undefined" src="../../public/default_profile.jpg" class="img-fluid">
            <img v-if="userProf?.logo !== undefined" :src='userProf?.logo' class="img-fluid">

            <div data-mdb-input-init class="form-outline mb-4">                        
                <label class="form-label" for="login">Изменить фото профиля</label>
                <input type="file" class="form-control" ref="taskImage" />
            </div>
        </div>

        <div class="col-6">

        </div>
    </div>
</template>