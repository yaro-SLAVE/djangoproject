<script setup lang="ts">
    import { computed, onBeforeMount, ref } from 'vue';
    import { storeToRefs } from 'pinia';
    import useUserProfileStore from '@/stores/userProfileStore';
    import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
    import { faBookmark } from '@fortawesome/free-regular-svg-icons';

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

    const testTopicType = ref("");

    const tasksToShow = ref({});

    onBeforeMount(async () => {
        await fetchAllTests();
    });

    async function fetchAllTests() {
        currentSection.value = "allTests";
    }

    async function fetchCurrentUserTests() {
        currentSection.value = "currentUserTests";
    }

    async function onTestToAdd() {
        
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
                <a class="btn btn-primary" data-toggle="collapse" :href="'#' + topicTypes.topic_type_name + 'Collapse'" role="button" aria-expanded="false" :aria-controls="topicTypes.topic_type_name + 'Collapse'">
                    {{ type.topic_type_name }}
                </a>
            </p>
              <div class="collapse" :id="type.topic_type_name + 'Collapse'">
                <div class="card card-body">
                    <div v-for="task in testsToShow">
                        <div>
                            
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
                    <h5 class="modal-title" id="addTaskModalLabel">Новое задание</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form class="d-flex flex-column justify-content-center mb-4" @submit.prevent.stop="onTestToAdd">

                        <div class="form-floating mb-4">
                            <select class="form-select" v-model="testTopicType" required>
                                <option :value="t.id" v-for="t in topicTypes">{{ t.topic_type_name }}</option>
                            </select>
                            <label for="floatingInput">Название темы теста</label>
                        </div>
                                            
                        <button class="btn btn-primary btn-block mb-4">Добавить тест</button>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                </div>
            </div>
        </div>
    </div>
</template>