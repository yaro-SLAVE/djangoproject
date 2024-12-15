<script setup lang="ts">
import {computed, ref, onBeforeMount, onActivated, onMounted} from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faGithub, faGooglePay, faGoogle, faYandex, faVk } from '@fortawesome/free-brands-svg-icons'
import axios from 'axios';
import useUserProfileStore from '@/stores/userProfileStore';
import router from "@/router";

const username = ref("");
const password = ref("");
const store = useUserProfileStore();

async function authenticate() {
  const auth = await store.login(username.value, password.value);
  if (auth) {
    store.getAuthInfo();
    store.getUserInfo();

    if (store.is_auth) {
      router.push('/');
    }
  } 
}

</script>

<template>
    <form @submit.prevent.stop="authenticate" class="d-flex flex-column justify-content-center mt-5 w-50">
      <div data-mdb-input-init class="form-outline mb-4">
        <label class="form-label" for="form2Example1">Логин</label>
        <input type="text" class="form-control" v-model="username" required />
      </div>
    
      <div data-mdb-input-init class="form-outline mb-4">
        <label class="form-label" for="form2Example2">Пароль</label>
        <input type="password" class="form-control"  v-model="password" required />
      </div>
    
      <button class="btn btn-primary btn-block mb-4">Ввойти</button>
    
      <div class="text-center">
        <p>Нет аккаунта? <a href="/registration">Зарегистрируйтесь</a></p>
        <p>Или войдите с помощью:</p>
        <button  type="button" data-mdb-button-init data-mdb-ripple-init class="btn btn-link btn-floating mx-1">
          <FontAwesomeIcon :icon="faGithub" />
        </button>
    
        <button  type="button" data-mdb-button-init data-mdb-ripple-init class="btn btn-link btn-floating mx-1">
          <FontAwesomeIcon :icon="faGoogle" />
        </button>
    
        <button  type="button" data-mdb-button-init data-mdb-ripple-init class="btn btn-link btn-floating mx-1">
          <FontAwesomeIcon :icon="faGooglePay" />
        </button>
    
        <button  type="button" data-mdb-button-init data-mdb-ripple-init class="btn btn-link btn-floating mx-1">
          <FontAwesomeIcon :icon="faVk" />
        </button>
      </div>
    </form>
</template>