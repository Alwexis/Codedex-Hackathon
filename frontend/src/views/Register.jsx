import { useState } from "react";

import Tooltip from "../components/Tooltip";

function Register() {
    const [formData, setFormData] = useState({});
    const [errors, setErrors] = useState({});

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
        validateField(e.target, name, value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(formData);
    };

    const validateField = (el, name, value) => {
        let error = "";
        if (name === "email" && !/\S+@\S+\.\S+/.test(value)) {
            error = "Use a valid email.";
            el.dataset.invalid = true;
        } else if (name === "password" && value.length < 6) {
            error = "Password must have at least 6 characters.";
            el.dataset.invalid = true;
        } else if (
            name === "username" &&
            (value.length < 3 || value.includes(" "))
        ) {
            error = "Username must have at least 3 characters with no spaces.";
            el.dataset.invalid = true;
        } else {
            el.dataset.invalid = null;
        }

        setErrors({ ...errors, [name]: error });
    };

    return (
        <main className="flex items-center justify-center h-screen w-full bg-gray-100 py-2 px-6">
            <div className="h-fit max-w-md mx-auto bg-white border-2 border-black p-6 shadow-[4px_4px_0_0_rgba(0,0,0,1)]">
                <h1 className="text-4xl font-bold mb-6 text-center">
                    Register
                </h1>
                <form onSubmit={handleSubmit} className="space-y-2">
                    {/* Username */}
                    <div>
                        <label
                            htmlFor="username"
                            className="block font-bold mb-1"
                        >
                            <span className="text-red-600 mr-1">*</span>
                            Username:
                        </label>
                        <input
                            onChange={handleChange}
                            id="username"
                            name="username"
                            className="w-full px-3 py-2 outline-none border-2 data-[invalid=true]:border-red-400 data-[invalid=true]:text-red-400 border-black transition-all bg-gray-100"
                            required
                            type="text"
                        />
                        {
                            errors.username && (
                                <p className="text-red-400 text-sm mt-1">
                                    {errors.username}
                                </p>
                            )
                        }
                    </div>
                    <div className="w-full flex items-center justify-between">
                        <div className="w-[45%]">
                            <label
                                htmlFor="email"
                                className="block font-bold mb-1"
                            >
                                <span className="text-red-600 mr-1">*</span>
                                Email:
                            </label>
                            <input
                                onChange={handleChange}
                                id="email"
                                name="email"
                                className="w-full px-3 py-2 outline-none border-2 data-[invalid=true]:border-red-400 data-[invalid=true]:text-red-400 border-black transition-all bg-gray-100"
                                required
                                type="email"
                            />
                        </div>
                        <div className="w-[45%]">
                            <label
                                htmlFor="password"
                                className="block font-bold mb-1"
                            >
                                <span className="text-red-600 mr-1">*</span>
                                Password:
                            </label>
                            <input
                                onChange={handleChange}
                                id="password"
                                name="password"
                                className="w-full px-3 py-2 outline-none border-2 data-[invalid=true]:border-red-400 data-[invalid=true]:text-red-400 border-black transition-all bg-gray-100"
                                required=""
                                type="password"
                            />
                        </div>
                    </div>
                    <div>
                        <label htmlFor="secret" className="flex w-full items-center justify-between font-bold mb-1">
                            <span>Secret:</span>
                            <Tooltip direction="bottom"
                                message={`Your "Secret" is something you can write down and let every single friend of yours know.`}>
                                <svg className="w-4 h-4 cursor-pointer text-neutral-800" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10s-4.477 10-10 10m0-2a8 8 0 1 0 0-16a8 8 0 0 0 0 16m1-9.5V15h1v2h-4v-2h1v-2.5h-1v-2zm.5-2.5a1.5 1.5 0 1 1-3 0a1.5 1.5 0 0 1 3 0"/></svg>
                            </Tooltip>
                        </label>
                        <input
                            onChange={handleChange}
                            id="secret"
                            name="secret"
                            className="w-full px-3 py-2 border-2 outline-none data-[invalid=true]:border-red-400 data-[invalid=true]:text-red-400 border-black transition-all bg-gray-100"
                            required=""
                            type="text"
                        />
                    </div>
                    <button
                        disabled={Object.values(errors).some((err) => err)}
                        type="submit"
                        className="cursor-pointer disabled:cursor-not-allowed w-full bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 border-b-2 border-green-700 hover:border-green-800 active:border-t-2 active:border-b-0 transition-all duration-100 mt-2"
                    >
                        Register
                    </button>
                </form>
                <p className="mt-4 text-center">
                    Already have an account?{" "}
                    <a href="/login" className="text-blue-600 underline">
                        Login here
                    </a>
                </p>
            </div>
        </main>
    );
}

export default Register;
