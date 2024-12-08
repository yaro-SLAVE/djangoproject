<script setup lang="ts">
    import { computed, onBeforeMount, ref } from 'vue';
    import { storeToRefs } from 'pinia';
    import useUserProfileStore from '@/stores/userProfileStore';
    import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
    import { faBookmark } from '@fortawesome/free-regular-svg-icons';
import axios from 'axios';

    const userStore = useUserProfileStore();

    const {
        userProf,
        jwt
    } = storeToRefs(userStore);

    const currentSectionId = ref<string>();

    const currentSection = computed({
        get(){
            return currentSectionId.value;
        },

        set(newSection: string){
            currentSectionId.value = newSection;
        }
    });



    const tasksToShow = ref({});
    const topicTypes = ref({});
    const answersTypes = ref({});

    const taskStatement = ref("");
    const taskImage = ref("");
    const taskTopicType = ref("");
    const answerA = ref("");
    const answerB = ref("");
    const answerC = ref("");
    const answerD = ref("");
    const correctAnswer = ref(0);
    const answersType = ref("");

    onBeforeMount(async () => {
        await fetchTopicTypes();
        await fetchTaskAnswersTypes();
        await fetchAllTasks();
    });

    async function fetchTopicTypes() {
        topicTypes.value = (await axios.get("/api/topic_type/")).data;
    }

    async function fetchTaskAnswersTypes() {
        answersTypes.value = (await axios.get("/api/task_answers_type/")).data;
    }

    async function fetchAllTasks() {
        currentSection.value = "allTasks";

        tasksToShow.value = (await axios.get("/api/task/?show=all", {
            headers: {
                Authorization: `Bearer ${jwt.value}`
            }
        })).data;
    }

    async function fetchCurrentUserTasks() {
        currentSection.value = "currentUserTasks";

        tasksToShow.value = (await axios.get("/api/task/?show=current_user", {
            headers: {
                Authorization: `Bearer ${jwt.value}`
            }
        })).data;
    }

    async function onTaskToAdd() {
        const body = {
            a: String(answerA.value),
            b: String(answerB.value),
            c: String(answerC.value),
            d: String(answerD.value)
        }

        const taskBody = JSON.stringify(body);

        const taskData = new FormData();

        taskData.append('task_statement', taskStatement.value);
        taskData.append('topic_type', taskTopicType.value);
        taskData.append('answers_type', answersType.value);
        taskData.append('task_body', taskBody);
        taskData.append('correct_answer', String(correctAnswer.value));

        const result = await axios.post("/api/task/", taskData, {
            headers: {
                Authorization: `Bearer ${jwt.value}`
            }
        });

        console.log(result);
    }
</script>

<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light w-100" v-if="userProf?.role === 'teacher'">
        <div class="container-fluid">
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTasks" aria-controls="navbarTasks" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarTasks">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0 d-flex flex-row">
                <li class="nav-item">
                    <button id="allTasks" class="btn" :class="{ 'btn-primary': currentSection === 'allTasks'}" v-on:click="fetchAllTasks()">
                        Все задания
                    </button>
                </li>

                <li class="nav-item">
                    <button id="currentUserTasks"  class="btn" :class="{ 'btn-primary': currentSection === 'currentUserTasks'}" v-on:click="fetchCurrentUserTasks()">
                        Мои задания
                    </button>
                </li>

                <li class="nav-item">
                    <button id="addTask" type="button" class="btn" data-bs-toggle="modal" data-bs-target="#addTaskModal">
                        + Добавить задание
                    </button>
                </li>
            </ul>
            </div>
        </div>
    </nav>

    <div class="mt-5 w-100">
        <div v-for="type in topicTypes">
            <p>
                <button class="btn" type="button" data-bs-toggle="collapse" :data-bs-target="'#' + type.id + 'Collapse'" aria-expanded="false" :aria-controls="type.id + 'Collapse'" role="button">
                    {{ type.topic_type_name }}
                </button>
            </p>
              <div class="collapse" :id="type.id + 'Collapse'">
                <div class="card card-body">
                    <div v-for="task in tasksToShow">
                        <div v-if="task.topic_type === type.id">
                            <label>{{ task.task_statement }}</label>
                        </div>
                    </div>
                </div>
              </div>
        </div>
    </div>

    <div class="modal fade" id="addTaskModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="addTaskModalLabel">Новое задание</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form class="d-flex flex-column justify-content-center mb-4" @submit.prevent.stop="onTaskToAdd">

                        <div class="row">
                            <div class="form-floating mb-4 col-6">
                                <select class="form-select" v-model="taskTopicType" required>
                                    <option :value="t.id" v-for="t in topicTypes">{{ t.topic_type_name }}</option>
                                </select>
                                <label for="floatingInput">Название темы задания</label>
                            </div>

                            <div class="form-floating mb-4 col-6">
                                <select class="form-select" v-model="answersType" required>
                                    <option :value="aT.id" v-for="aT in answersTypes">{{ aT.description }}</option>
                                </select>
                                <label for="floatingInput">Тип ответов</label>
                            </div>
                        </div>

                        <div data-mdb-input-init class="form-outline mb-4">                        
                          <label class="form-label" for="login">Условие задания</label>
                          <textarea class="form-control" id="exampleFormControlTextarea1" rows="3" v-model="taskStatement" required></textarea>
                        </div>

                        <div data-mdb-input-init class="form-outline mb-4">                        
                            <label class="form-label" for="login">Изображение к заданию</label>
                            <input type="file" class="form-control" ref="taskImage" />
                        </div>

                        <div data-mdb-input-init class="form-outline mb-4">
                            <label class="form-label" for="form2Example1">a{{')'}}</label>
                            <input type="text" class="form-control" v-model="answerA" required />
                        </div>

                        <div data-mdb-input-init class="form-outline mb-4">
                            <label class="form-label" for="form2Example1">b{{')'}}</label>
                            <input type="text" class="form-control" v-model="answerB" required />
                        </div>

                        <div data-mdb-input-init class="form-outline mb-4">
                            <label class="form-label" for="form2Example1">c{{')'}}</label>
                            <input type="text" class="form-control" v-model="answerC" required />
                        </div>

                        <div data-mdb-input-init class="form-outline mb-4">
                            <label class="form-label" for="form2Example1">d{{')'}}</label>
                            <input type="text" class="form-control" v-model="answerD" required />
                        </div>

                        <div>
                            <label>Выберите верный ответ</label>
                            <div class="row">
                                <div class="col-6">
                                    <div class="form-check">
                                        <input class="form-check-input" type="radio" name="flexRadioDefault" id="answerA" v-model="correctAnswer" :value="0" checked>
                                        <label class="form-check-label" for="answerA">
                                            a
                                        </label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="radio" name="flexRadioDefault" id="answerB" v-model="correctAnswer" :value="1">
                                        <label class="form-check-label" for="answerB">
                                            b
                                        </label>
                                    </div>
                                </div>

                                <div class="col-6">
                                    <div class="form-check">
                                        <input class="form-check-input" type="radio" name="flexRadioDefault" id="answerC" v-model="correctAnswer" :value="2">
                                        <label class="form-check-label" for="answerC">
                                            c
                                        </label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="radio" name="flexRadioDefault" id="answerD" v-model="correctAnswer" :value="3">
                                        <label class="form-check-label" for="answerD">
                                            d
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>
                                            
                        <button class="btn btn-primary btn-block mb-4">Добавить задание</button>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                </div>
            </div>
        </div>
    </div>
</template>