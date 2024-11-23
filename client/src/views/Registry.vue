<script setup lang="ts">

</script>

<template>
  <form class="d-flex flex-column justify-content-center">
    <div data-mdb-input-init class="form-outline mb-4">
      <input type="email" id="form2Example1" class="form-control" />
      <label class="form-label" for="form2Example1">Логин</label>
    </div>
  
    <div data-mdb-input-init class="form-outline mb-4">
      <input type="password" id="form2Example2" class="form-control" />
      <label class="form-label" for="form2Example2">Пароль</label>
    </div>
  
    <button  type="button" data-mdb-button-init data-mdb-ripple-init class="btn btn-primary btn-block mb-4">Sign up</button>
  
    <div class="text-center">
      <p>Have an account? <a href="/login">Sign in</a></p>
    </div>
  </form>
</template>