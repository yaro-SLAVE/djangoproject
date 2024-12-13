<script setup lang="ts">
    import { computed, onBeforeMount, ref } from 'vue';
    import { storeToRefs } from 'pinia';
    import useUserProfileStore from '@/stores/userProfileStore';
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

    const taskStatement = ref();
    const taskImage = ref();
    const taskImageURL = ref();
    const taskTopicType = ref();

    const answerA = ref();
    const answerB = ref();
    const answerC = ref();
    const answerD = ref();

    const correctAnswer = ref(0);
    const answersType = ref();

    const imageA = ref();
    const imageB = ref();
    const imageC = ref();
    const imageD = ref();

    const imageAURL = ref();
    const imageBURL = ref();
    const imageCURL = ref();
    const imageDURL = ref();

    const currentTask = ref();

    const images = ref({});

    onBeforeMount(async () => {
        await fetchTopicTypes();
        await fetchTaskAnswersTypes();
        await fetchAllTasks();
        await fetchImages();
    });

    async function fetchImages() {
        images.value = (await axios.get("/api/image/")).data;
    }

    async function changeAnswersImages() {
        imageAURL.value = URL.createObjectURL(imageA.value.files[0]);
        imageBURL.value = URL.createObjectURL(imageB.value.files[0]);
        imageCURL.value = URL.createObjectURL(imageC.value.files[0]);
        imageDURL.value = URL.createObjectURL(imageD.value.files[0]);
    }

    async function changeTaskImage() {
        taskImageURL.value = URL.createObjectURL(taskImage.value.files[0]);
    }

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
        const taskData = new FormData();

        taskData.append('task_statement', taskStatement.value);
        taskData.append('topic_type', taskTopicType.value);
        taskData.append('answers_type', answersType.value.id);
        taskData.append('correct_answer', String(correctAnswer.value));

        if (taskImage.value.files[0] != undefined) {
            const imageForm = new FormData();

            imageForm.append('image', taskImage.value.files[0]);

            const image = (await axios.post("/api/image/", imageForm, {
                headers: {
                    Authorization: `Bearer ${jwt.value}`
                }
            })).data;

            taskData.append('task_image', image.id);
        }

        if (answersType.value.type_name === 'text') {
            const body = {
                a: String(answerA.value),
                b: String(answerB.value),
                c: String(answerC.value),
                d: String(answerD.value)
            }

            const taskBody = JSON.stringify(body);

            taskData.append('task_body', taskBody);

            answerA.value = "";
            answerB.value = "";
            answerC.value = "";
            answerD.value = "";
        } else if (answersType.value.type_name === 'image') {
            const aBody = new FormData();
            const bBody = new FormData();
            const cBody = new FormData();
            const dBody = new FormData();

            aBody.append('image', imageA.value.files[0]);
            bBody.append('image', imageB.value.files[0]);
            cBody.append('image', imageC.value.files[0]);
            dBody.append('image', imageD.value.files[0]);

            const answA = (await axios.post("/api/image/", aBody, {
                headers: {
                    Authorization: `Bearer ${jwt.value}`
                }
            })).data;

            const answB = (await axios.post("/api/image/", bBody, {
                headers: {
                    Authorization: `Bearer ${jwt.value}`
                }
            })).data;

            const answC = (await axios.post("/api/image/", cBody, {
                headers: {
                    Authorization: `Bearer ${jwt.value}`
                }
            })).data;

            const answD = (await axios.post("/api/image/", dBody, {
                headers: {
                    Authorization: `Bearer ${jwt.value}`
                }
            })).data;

            const body = {
                a: String(answA.id),
                b: String(answB.id),
                c: String(answC.id),
                d: String(answD.id)
            }

            const taskBody = JSON.stringify(body);

            taskData.append('task_body', taskBody);

            imageA.value = "";
            imageB.value = "";
            imageC.value = "";
            imageD.value = "";
        }

        const result = await axios.post("/api/task/", taskData, {
            headers: {
                Authorization: `Bearer ${jwt.value}`
            }
        });

        taskStatement.value = "";
        taskImage.value = "";
        taskTopicType.value = "";
        answersType.value = "";
        correctAnswer.value = 0;

        await fetchCurrentUserTasks();
    }

    async function updateCurrentTask(task) {
        currentTask.value = task;
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
                        <button type="button" class="btn" data-bs-toggle="modal" data-bs-target="#taskModal" v-on:click="updateCurrentTask(task)">
                            <div v-if="task.topic_type === type.id">
                                <vue-mathjax :formula="task.task_statement"></vue-mathjax>
                            </div>
                        </button>
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
                                    <option :value="aT" v-for="aT in answersTypes">{{ aT.description }}</option>
                                </select>
                                <label for="floatingInput">Тип ответов</label>
                            </div>
                        </div>

                        <div data-mdb-input-init class="form-outline mb-4">                        
                          <label class="form-label" for="login">Условие задания</label>
                          <textarea class="form-control" id="exampleFormControlTextarea1" rows="3" v-model="taskStatement" required></textarea>
                          <vue-mathjax :formula="taskStatement"></vue-mathjax>
                        </div>

                        <div data-mdb-input-init class="form-outline mb-4">                        
                            <label class="form-label" for="login">Изображение к заданию</label>
                            <input type="file" class="form-control col-6" ref="taskImage" @change="changeTaskImage()"/>
                            <div class="task-image-wrap my-4 text-center col-6">
                                <img :src="taskImageURL" class="img-fluid" style="height: 100%">
                            </div>
                        </div>

                        <div v-if="answersType?.type_name === 'text'">
                            <div data-mdb-input-init class="form-outline mb-4">
                                <label class="form-label" for="form2Example1">a{{')'}}</label>
                                <input type="text" class="form-control" v-model="answerA" required />
                                <vue-mathjax class="my-5" :formula="answerA"></vue-mathjax>
                            </div>
    
                            <div data-mdb-input-init class="form-outline mb-4">
                                <label class="form-label" for="form2Example1">b{{')'}}</label>
                                <input type="text" class="form-control" v-model="answerB" required />
                                <vue-mathjax class="my-5" :formula="answerB"></vue-mathjax>
                            </div>
    
                            <div data-mdb-input-init class="form-outline mb-4">
                                <label class="form-label" for="form2Example1">c{{')'}}</label>
                                <input type="text" class="form-control" v-model="answerC" required />
                                <vue-mathjax class="my-5" :formula="answerC"></vue-mathjax>
                            </div>
    
                            <div data-mdb-input-init class="form-outline mb-4">
                                <label class="form-label" for="form2Example1">d{{')'}}</label>
                                <input type="text" class="form-control" v-model="answerD" required />
                                <vue-mathjax class="my-5" :formula="answerD"></vue-mathjax>
                            </div>
                        </div>

                        <div v-if="answersType?.type_name === 'image'">
                            <div class="my-4 row">
                                <label class="form-label">a{{')'}}</label>
                                <input type="file" class="form-control col-6" ref="imageA" @change="changeAnswersImages()"/>
                                <div class="task-image-wrap my-4 text-center col-6">
                                    <img :src="imageAURL" class="img-fluid" style="height: 100%">
                                </div>
                            </div>

                            <div class="my-4 row">
                                <label class="form-label">b{{')'}}</label>
                                <input type="file" class="form-control col-6" ref="imageB" @change="changeAnswersImages()"/>
                                <div class="task-image-wrap my-4 text-center col-6">
                                    <img :src="imageBURL" class="img-fluid" style="height: 100%">
                                </div>
                            </div>

                            <div class="my-4 row">
                                <input type="file" class="form-control col-6" ref="imageC" @change="changeAnswersImages()"/>
                                <div class="task-image-wrap my-4 text-center col-6">
                                    <img :src="imageCURL" class="img-fluid" style="height: 100%">
                                </div>
                            </div>

                            <div class="my-4 row">
                                <label class="form-label">d{{')'}}</label>
                                <input type="file" class="form-control col-6" ref="imageD" @change="changeAnswersImages()"/>
                                <div class="task-image-wrap my-4 text-center col-6">
                                    <img :src="imageDURL" class="img-fluid" style="height: 100%">
                                </div>
                            </div>
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
                                            
                        <button class="btn btn-primary btn-block mb-4" data-bs-dismiss="modal">Добавить задание</button>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" id="taskModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body" v-if="currentTask !== undefined">
                    <vue-mathjax class="mt-4" :formula="currentTask.task_statement"></vue-mathjax>
                    <div class="task-image-wrap my-4" v-if="currentTask.task_image !== undefined">
                        <img class="img-fluid" :src="currentTask.task_image" style="height: 100%">
                    </div>

                    <div class="row my-4 d-flex flex-row align-items-center">
                        <label class="col-2">a{{')'}}</label>
                        <vue-mathjax class="col-10" :formula="currentTask.task_body.a"></vue-mathjax>
                    </div>

                    <div class="row my-4 d-flex flex-row align-items-center">
                        <label class="col-2">b{{')'}}</label>
                        <vue-mathjax class="col-10" :formula="currentTask.task_body.b"></vue-mathjax>
                    </div>

                    <div class="row my-4 d-flex flex-row align-items-center">
                        <label class="col-2">c{{')'}}</label>
                        <vue-mathjax class="col-10" :formula="currentTask.task_body.c"></vue-mathjax>
                    </div>

                    <div class="row my-4 d-flex flex-row align-items-center">
                        <label class="col-2">d{{')'}}</label>
                        <vue-mathjax class="col-10" :formula="currentTask.task_body.d"></vue-mathjax>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .task-image-wrap {
        width: 120px; 
        height: 120px; 
        border-radius: 15px;
        overflow: hidden;
    }
</style>