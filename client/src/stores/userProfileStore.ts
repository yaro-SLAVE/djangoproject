import {defineStore} from "pinia"
import {computed, ref, onBeforeMount} from 'vue';
import axios from "axios";

const useUserProfileStore = defineStore("UserProfileStore", () => {
    const is_auth = ref();
    const is_superuser = ref();
    const username = ref();

    onBeforeMount(async () => {
        const user = await axios.get("api/users/info");
        is_auth.value = user.data.is_authenticated;
        username.value = user.data.username;
        is_superuser.value = user.data.is_superuser;
    });

    return {is_auth, is_superuser, username};
})

export default useUserProfileStore;