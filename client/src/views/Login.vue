<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faChartPie, faCreditCard, faGrin }  from '@fortawesome/free-solid-svg-icons'
import { faGithub, faGooglePay, faGoogle, faYandex, faVk } from '@fortawesome/free-brands-svg-icons'
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
    
      <button  type="button" data-mdb-button-init data-mdb-ripple-init class="btn btn-primary btn-block mb-4">Sign in</button>
    
      <div class="text-center">
        <p>Not a member? <a href="/registration">Register</a></p>
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