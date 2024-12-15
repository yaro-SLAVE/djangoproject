<script setup lang="ts">
  import router from '@/router';
import useUserProfileStore from '@/stores/userProfileStore';
  import { faGithub, faGoogle, faGooglePay, faVk } from '@fortawesome/free-brands-svg-icons';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import axios from 'axios';
  import { onBeforeMount, ref } from 'vue';

  const roles = ref({});
  const groups = ref({});

  const username = ref();
  const password = ref();
  const email = ref();
  const firstName = ref();
  const lastName = ref();
  const role = ref();
  const group = ref()

  const userStore = useUserProfileStore();

  onBeforeMount(async () => {
    fetchRoles();
    fetchGroups();
  });

  async function fetchRoles() {
    roles.value = (await axios.get("/api/role/")).data;
    
  }

  async function fetchGroups() {
    groups.value = (await axios.get("/api/group/")).data;
  }

  async function onUserToAdd() {
    const result = await userStore.registry(username.value, password.value, firstName.value, lastName.value, email.value, role.value.id);

    if (result){
      const login = await userStore.login(username.value, password.value);

      if (login) {
        router.push('/');
      }
    }
  }

</script>

<template>
  <form class="d-flex flex-column justify-content-center mt-5" @submit.prevent.stop="onUserToAdd">
    <div data-mdb-input-init class="form-outline mb-4">
      <label class="form-label" for="login">Логин</label>
      <input type="text" id="login" class="form-control" v-model="username" required />
    </div>
  
    <div data-mdb-input-init class="form-outline mb-4">
      <label class="form-label" for="password">Пароль</label>
      <input type="password" id="password" class="form-control" v-model="password" required  />
    </div>

    <div data-mdb-input-init class="form-outline mb-4">
      <label class="form-label" for="email">E-mail</label>
      <input type="email" id="email" class="form-control" v-model="email" />
    </div>

    <div class="row">
      <div class="col-6">
        <div data-mdb-input-init class="form-outline mb-4" >
          <label class="form-label" for="firstName">Имя</label>
          <input type="text" id="firstName" class="form-control" v-model="firstName" required />
        </div>
      </div>

      <div class="col-6">
        <div data-mdb-input-init class="form-outline mb-4" >
          <label class="form-label" for="lastName">Фамилия</label>
          <input type="text" id="lastName" class="form-control" v-model="lastName" required />
        </div>
      </div>
    </div>

    <div class="row">
      <div class="form-floating col-6">
        <select class="form-select" v-model="role" required>
          <option :value="r" v-for="r in roles">{{ r.description }}</option>
        </select>
        <label for="floatingInput">Ваша роль</label>
      </div>

      <div class="form-floating col-6" v-if="role?.role === 'student'">
        <select class="form-select" v-model="group" required>
          <option :value="g" v-for="g in groups">{{ g.group_name }}</option>
        </select>
        <label for="floatingInput">Ваша группа</label>
      </div>
    </div>
  
    <button class="btn btn-primary btn-block my-4">Зарегистрироваться</button>

    <div class="text-center">
      <p>Уже зарегистрированы? <a href="/login">Войдите</a></p>
      <p>Или зарегистрируйтесь с помощью:</p>
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