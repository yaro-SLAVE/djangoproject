<script setup lang="ts">
  import type { ProfileToAdd } from '@/customTypes';
import useUserProfileStore from '@/stores/userProfileStore';
import { faGithub, faGoogle, faGooglePay, faVk } from '@fortawesome/free-brands-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import axios from 'axios';
  import { onBeforeMount, ref } from 'vue';

  const roles = ref({});

  const username = ref("");
  const password = ref("");
  const email = ref("");
  const first_name = ref("");
  const last_name = ref("");
  const role = ref("");

  const userStore = useUserProfileStore();

  onBeforeMount(async () => {
    fetchRoles();
  });

  async function fetchRoles() {
    roles.value = (await axios.get("/api/roles")).data;
  }

  async function onUserToAdd() {

  }

</script>

<template>
  <form class="d-flex flex-column justify-content-center mt-5" @submit.prevent.stop="onUserToAdd">
    <div data-mdb-input-init class="form-outline mb-4">
      <input type="text" id="login" class="form-control" v-model="username" required />
      <label class="form-label" for="login">Логин</label>
    </div>
  
    <div data-mdb-input-init class="form-outline mb-4">
      <input type="password" id="password" class="form-control" v-model="password" required  />
      <label class="form-label" for="password">Пароль</label>
    </div>

    <div data-mdb-input-init class="form-outline mb-4">
      <input type="email" id="email" class="form-control" v-model="email" />
      <label class="form-label" for="email">E-mail</label>
    </div>

    <div class="row">
      <div class="col-6">
        <div data-mdb-input-init class="form-outline mb-4" >
          <input type="text" id="first_name" class="form-control" v-model="first_name" required />
          <label class="form-label" for="first_name">Имя</label>
        </div>
      </div>

      <div class="col-6">
        <div data-mdb-input-init class="form-outline mb-4" >
          <input type="text" id="last_name" class="form-control" v-model="last_name" required />
          <label class="form-label" for="last_name">Фамилия</label>
        </div>
      </div>
    </div>

    <div class="form-floating">
      <select class="form-select" v-model="role" required>
        <option :value="r.id" v-for="r in roles">{{ r.role }}</option>
      </select>
      <label for="floatingInput">Ваша роль</label>
    </div>
  
    <button  type="button" data-mdb-button-init data-mdb-ripple-init class="btn btn-primary btn-block my-4">Sign up</button>

    <div class="text-center">
      <p>Have an account? <a href="/login">Sign in</a></p>
      <p>or sign up with:</p>
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