<script setup lang="ts">
    import { computed, onBeforeMount, ref } from 'vue';
    import { storeToRefs } from 'pinia';
    import useUserProfileStore from '@/stores/userProfileStore';
    import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
    import { faBookmark, faTrashAlt } from '@fortawesome/free-regular-svg-icons';
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

    const testsToShow = ref({});
    const topicTypes = ref({});

    const testTopicType = ref();

    const tasksToAddToShow = ref({});

    const tasksToAdd = ref([]);

    const testName = ref("");

    onBeforeMount(async () => {
        await fetchAllTests();
        await fetchTopicTypes();
        await fetchTasks();
    });

    async function fetchTasks() {
        tasksToAddToShow.value = (await axios.get("/api/task/?show=all", {
            headers: {
                Authorization: `Bearer ${jwt.value}`
            }
        })).data;
    }

    async function fetchTopicTypes() {
        topicTypes.value = (await axios.get("/api/topic_type/")).data;
    }

    async function fetchAllTests() {
        currentSection.value = "allTests";

        testsToShow.value = (await axios.get("/api/test/?show=all", {
            headers: {
                Authorization: `Bearer ${jwt.value}`
            }
        })).data;
    }

    async function fetchCurrentUserTests() {
        currentSection.value = "currentUserTests";

        testsToShow.value = (await axios.get("/api/test/?show=current_user", {
            headers: {
                Authorization: `Bearer ${jwt.value}`
            }
        })).data;
    }

    async function changeTasks(task){
        if (tasksToAdd.value.includes(task.id)) {
            const index = tasksToAdd.value.findIndex((item)=>{return (item === task.id)});
            tasksToAdd.value.splice(index, 1);
        } else {
            tasksToAdd.value.push(task.id);
        }
    }

    async function changeTopicType() {
        const length = tasksToAdd.value.length;
        tasksToAdd.value.splice(0, length);
    }

    async function onTestToAdd() {
        if (tasksToAdd.value.length > 0) {
            const testData = new FormData();

            testData.append('topic_type', testTopicType.value);
            testData.append('name', testName.value);

            const test = (await axios.post("/api/test/", testData, {
                headers: {
                    Authorization: `Bearer ${jwt.value}`
                },
            })).data;

            tasksToAdd.value.forEach(async (item) => {
                const testTaskData = new FormData();

                testTaskData.append('test', test.id);
                testTaskData.append('task', item);

                await axios.post("/api/test_task/", testTaskData, {
                    headers: {
                        Authorization: `Bearer ${jwt.value}`
                    },
                })  
            });
        }

        await fetchAllTests();

        testName.value = "";

        const length = tasksToAdd.value.length;
        tasksToAdd.value.splice(0, length);

        testTopicType.value = "";
    }

    async function deleteTest(id: number) {
        await axios.delete("/api/test/" + id + "/", {
            headers: {
                    Authorization: `Bearer ${jwt.value}`
            }
        });

        await fetchCurrentUserTests();
    }
</script>

<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light w-100" v-if="userProf?.role === 'teacher'">
        <div class="container-fluid">
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTests" aria-controls="navbarTests" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarTests">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0 d-flex flex-row">
                <li class="nav-item">
                    <button id="allTasks" class="btn" :class="{ 'btn-primary': currentSection === 'allTests'}" v-on:click="fetchAllTests()">
                        Все тесты
                    </button>
                </li>

                <li class="nav-item">
                    <button id="currentUserTasks"  class="btn" :class="{ 'btn-primary': currentSection === 'currentUserTests'}" v-on:click="fetchCurrentUserTests()">
                        Мои тесты
                    </button>
                </li>

                <li class="nav-item">
                    <button id="addTask" type="button" class="btn" data-bs-toggle="modal" data-bs-target="#addTestModal">
                        + Добавить тест
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
                    <div v-for="test in testsToShow">
                        <div v-if="test.topic_type === type.id" class="d-flex flex-row row align-items-center justify-content-between">
                            <label class="col-6 mx-5">{{test.name}}</label>

                            <div class="col-2" v-if="currentSection === 'currentUserTests' || userProf?.role === 'admin'">
                                <button type="button" class="btn btn-danger" v-on:click="deleteTest(test.id)">
                                    <FontAwesomeIcon :icon="faTrashAlt"></FontAwesomeIcon>
                                </button>
                            </div>

                            <hr class="my-5 mx-5 w-75">
                        </div>                        
                    </div>
                </div>
              </div>
        </div>
    </div>

    <div class="modal fade" id="addTestModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="addTaskModalLabel">Новый тест</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form class="d-flex flex-column justify-content-center mb-4" @submit.prevent.stop="onTestToAdd">

                        <div data-mdb-input-init class="form-outline mb-4">
                            <label class="form-label">Название теста</label>
                            <input type="text" class="form-control" v-model="testName" required />
                        </div>

                        <div class="form-floating mb-4">
                            <select class="form-select" v-model="testTopicType" @change="changeTopicType()" required>
                                <option :value="t.id" v-for="t in topicTypes">{{ t.topic_type_name }}</option>
                            </select>
                            <label for="floatingInput">Название темы теста</label>
                        </div>

                        <div class="form-floating mb-4" v-for="task in tasksToAddToShow">
                            <div class="form-check" v-if="testTopicType !== undefined && task.topic_type === testTopicType">
                                <vue-mathjax :formula="task.task_statement"></vue-mathjax>
                                <input class="form-check-input" type="checkbox" @change="changeTasks(task)">
                            </div>
                        </div>
                                            
                        <button class="btn btn-primary btn-block mb-4" data-bs-dismiss="modal">Добавить тест</button>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
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