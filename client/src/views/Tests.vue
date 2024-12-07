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

    onBeforeMount(async () => {
        await fetchAllTests();
    });

    async function fetchAllTests() {
        currentSection.value = "allTasks";
    }

    async function fetchCurrentUserTests() {
        currentSection.value = "currentUserTasks";
    }
</script>

<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light w-100">
        <div class="container-fluid">
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTests" aria-controls="navbarTests" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarTests">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0 d-flex flex-row">
                <li class="nav-item">
                    <button id="allTests" class="btn" :class="{ 'btn-primary': currentSection === 'allTasks'}" @submit.prevent.stop="fetchAllTests">
                        Все тесты
                    </button>
                </li>

                <li class="nav-item" >
                    <button id="currentUserTests"  class="btn" :class="{ 'btn-primary': currentSection === 'currentUserTasks'}" @submit.prevent.stop="fetchCurrentUserTests">
                        Мои тесты
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
</template>