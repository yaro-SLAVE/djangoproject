export type User = {
    is_authenticated: boolean;
    is_superuser: boolean;
    username: string;
    first_name: string;
    last_name: string;
    role: string;
    logo: string;
};