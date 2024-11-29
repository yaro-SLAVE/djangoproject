import {defineStore} from "pinia"
import {computed, ref, onBeforeMount} from 'vue';
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import { useLocalStorage } from "@vueuse/core";
import type { RefSymbol } from "@vue/reactivity";
import type { User} from "@/CustomTypes"

const useUserProfileStore = defineStore("UserProfileStore", () => {
    type Tokens = {
        access: string;
        refresh: string;
    };

    type Token = string | undefined;
    
    const userProf = ref<User>();

    const jwt = useLocalStorage<Token>("jwt", undefined);
    const refresh = useLocalStorage<Token>("refresh", undefined);

    function isTokenValid(token: Token): boolean {
        if (jwt === undefined) {
            return false;
        } else {
            const decoded = jwtDecode(token);
            return Date.now() < decoded.exp! * 1000;
        }
    }

    async function login(username: string, password: string): Promise<boolean> {      
        try {
            const result = (
                await axios.post<Tokens>("/api/auth/", {
                    username: username,
                    password: password,
                })
            ).data;

            jwt.value = result.access;
            refresh.value = result.refresh;

            await getUserInfo();
            return true;
        } catch(error){
            console.error("При авторизации ошибка", error);
            return false;
        }
    }

    async function registry() {

    }

    async function logout() {

    }

    async function updateTokens(): Promise<boolean> {
        if (!isTokenValid(refresh.value)) {
            refresh.value = undefined;
            jwt.value = undefined;
            userProf.value = undefined;
            return false;
        } else if (!isTokenValid(jwt.value)) {
            await refreshTokens();
        }

        return true;
    }

    async function refreshTokens() {
        const simpleAxios = axios.create();
        const newTokens: Tokens = (
        await simpleAxios.post("/api/auth/refresh", {
                refresh: refresh.value,
            })
        ).data;

        jwt.value = newTokens.access;
        refresh.value = newTokens.refresh;
    }

    async function getUserInfo() {
        if (await updateTokens()) {
            try {
                userProf.value = (await axios.get("/api/profiles/info", {
                    headers: {
                        Authorization: `Bearer ${jwt.value}`
                    },
                })).data;

                console.log(userProf.value?.is_authenticated)
            } catch(error) {
                console.error("Ошибка при получении инфы о пользователе", error);
            }
            console.log(userProf.value?.is_authenticated)
        }
    }

    onBeforeMount(async () => {
        await getUserInfo();
    });

    return {userProf, jwt, login};
});

export default useUserProfileStore;