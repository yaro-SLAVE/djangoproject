<script setup lang="ts">
    import { storeToRefs } from 'pinia';
    import useUserProfileStore from '../stores/userProfileStore';

    const userProfileStore = useUserProfileStore();

    const {
        userProf
    } = storeToRefs(userProfileStore);
</script>

<template>
    <h1 class="my-5 text-center">Добро пожаловать на мой сайт по созданию тестов по высшей математике!</h1>
    <h3 v-if="userProf?.role === 'student'">Вы зарегистрированы как <b>студент</b>, поэтому вам доступен только просмотр банков вопросов и тестов!</h3>
    <h3 v-if="userProf?.role === 'teacher'">Вы зарегистрированы как <b>преподаватель</b>, поэтому вам доступно следующее:</h3>
    <lu v-if="userProf?.role === 'teacher'" class="my-5" style="font-size: 25px">
        <li>Просмотр банков заданий и тестов</li>
        <li>Создание собственных заданий и тестов</li>
        <li>Изменение и удаление собственных заданий и тестов</li>
    </lu>
</template>
