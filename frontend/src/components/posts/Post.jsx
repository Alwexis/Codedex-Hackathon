import { useAuth } from "../../contexts/AuthContext";

export default function Posts({ post, isSelfPost, showAuthor, onPostLike, onPinPost, onPostDelete }) {
    const { user } = useAuth();
    //? Ya que la fecha que genera PyDantic por defecto está en un formato distinto, la transformaremos a un formato más legible
    //? El formato para mostrar será "DD/MM/YYYY HH:MM"
    const normalDate = new Date(post.fecha.$date);
    let _date = normalDate.toLocaleDateString().replaceAll('-', '/');
    let _hours = normalDate.getHours() < 10 ? `0${normalDate.getHours()}` : normalDate.getHours();
    let _minutes = normalDate.getMinutes() < 10 ? `0${normalDate.getMinutes()}` : normalDate.getMinutes();
    let _time = `${_hours}:${_minutes}`;
    const date = `${_date} ${_time}`;

    return (
        <div className={`${showAuthor ? "flex items-start" : ""} bg-gray-100 p-4 border-2 border-black`}>
            {showAuthor && (
                <div className="max-w-12 flex flex-col items-center justify-center">
                    <img
                        src={post.user.profile_picture}
                        alt=""
                        className="w-12 h-12 object-contain border-2 border-black"
                    />
                    <span className="text-sm">{post.user.username}</span>
                </div>
            )}
            <div className="ml-4 w-full">
                <h3 className="font-bold">{post.title}</h3>
                <p className="text-sm">{post.content}</p>
                {isSelfPost ? (
                    <>
                        {post.files && post.files.length > 0 && (
                            <div className="my-2 grid grid-cols-2 gap-2 md:flex md:items-center">
                                {post.files.map((file, index) => (
                                    <a key={index} href={file} target="_blank" rel="noreferrer">
                                        <img className="w-24 h-24 object-contain hover:scale-105 transition-all" src={file} alt="uploaded_file" />
                                    </a>
                                ))}
                            </div>
                        )}
                        <div className="w-full flex items-center justify-between">
                            <p className="text-sm text-red-600 mt-2">
                                ♥ {post.likes.length} Likes
                            </p>
                            <p className="text-gray-400 text-xs mt-2">
                                {date}
                            </p>
                        </div>
                        <div className="mt-2 space-x-2">
                            <button className="bg-blue-500 hover:bg-blue-400 transition-all cursor-pointer text-white px-2 py-1 text-sm">
                                {post.isPinned ? "Unpin" : "Pin"}
                            </button>
                            <button onClick={() => onPostDelete(post.id)} className="bg-red-500 hover:bg-red-400 transition-all cursor-pointer text-white px-2 py-1 text-sm">
                                Delete
                            </button>
                        </div>
                    </>
                ) : (
                    <>
                        {post.files.length > 0 && (
                            <div className="my-2 grid grid-cols-2 gap-2 md:flex md:items-center">
                                {post.files.map((file, index) => (
                                    <a key={index} href={file} target="_blank" rel="noreferrer">
                                        <img className="w-24 h-24 object-contain hover:scale-105 transition-all" src={file} alt="uploaded_file" />
                                    </a>
                                ))}
                            </div>
                        )}
                        <div className="w-full flex items-center justify-between">
                            <p
                                onClick={() => onPostLike(post.id)}
                                className={`${
                                    post.likes.includes(user.uid)
                                        ? "text-red-600"
                                        : "text-gray-800"
                                } text-sm mt-2 cursor-pointer`}
                            >
                                ♥ {post.likes.length} Likes
                            </p>
                            <p className="text-xs mt-2">{date}</p>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
}
