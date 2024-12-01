export type User = {
    is_authenticated: boolean;
    is_superuser: boolean;
    username: string;
    role: string;
    logo: string;
};

export type UserToAdd = {
    username: string;
    password: string;
    email: string;
    first_name: string;
    last_name: string;
};

export type ProfileToAdd = {
    user: UserToAdd;
    role: number;
};