import {defineStore} from "pinia"
import {computed, ref, onBeforeMount} from 'vue';
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import { useLocalStorage } from "@vueuse/core";
import type { RefSymbol } from "@vue/reactivity";
import type { User} from "@/customTypes"
import router from "@/router";

const useUserProfileStore = defineStore("UserProfileStore", () => {
    type Tokens = {
        access: string;
        refresh: string;
    };

    type Token = string | undefined;
    
    const userProf = ref<User>();

    const jwt = useLocalStorage<Token>("jwt", undefined);
    const refresh = useLocalStorage<Token>("refresh", undefined);

    const is_auth = useLocalStorage<boolean>("authorization", false);

    function isTokenValid(token: Token): boolean {
        if (token === undefined) {
            return false;
        } else {
            const decoded = jwtDecode(String(token));
            return Date.now() < decoded.exp! * 1000;
        }
    }

    async function login(username: string, password: string): Promise<boolean> {      
        try {
            const result = (
                await axios.post<Tokens>("/api/auth/login/", {
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
        const refreshCopy = refresh.value;
        refresh.value = undefined;
        jwt.value = undefined;
        userProf.value = undefined;
        is_auth.value = false;

        await axios.post("/api/auth/logout/", {
            headers: {
                Authorization: `Bearer ${jwt.value}`
            },
            refresh: refreshCopy,
        });

        await axios.post("/admin/logout/")

        router.push('/login');
    }

    async function updateTokens(): Promise<boolean> {
        if (!isTokenValid(refresh.value)) {
            refresh.value = undefined;
            jwt.value = undefined;
            userProf.value = undefined;
            is_auth.value = false;
            return false;
        } else if (!isTokenValid(jwt.value)) {
            await refreshTokens();
        }

        return true;
    }

    async function refreshTokens() {
        const simpleAxios = axios.create();
        const newTokens: Tokens = (
        await simpleAxios.post("/api/auth/refresh/", {
                refresh: refresh.value,
            })
        ).data;

        jwt.value = newTokens.access;
        refresh.value = newTokens.refresh;
    }

    async function getUserInfo() {
        if (await updateTokens()) {
            try {
                userProf.value = (await axios.get<User>("/api/profile/info/", {
                    headers: {
                        Authorization: `Bearer ${jwt.value}`
                    },
                })).data;

                is_auth.value = userProf.value.is_authenticated;
            } catch(error) {
                console.error("Ошибка при получении инфы о пользователе", error);
            }
        }
    }

    onBeforeMount(async () => {
        await getUserInfo();
    });

    return {userProf, jwt, is_auth, login, logout};
});

export default useUserProfileStore;