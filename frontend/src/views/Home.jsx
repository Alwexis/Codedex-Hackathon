import { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { auth } from '../firebase'
import Loading from '../components/Loading'

export default function Home() {
  const { user, firebaseUser, loading } = useAuth()
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [activeTab, setActiveTab] = useState('posts')
  const [searchQuery, setSearchQuery] = useState('')
  console.log(user)

  // Dummy data
  const posts = [
    { id: 1, user: 'user1', title: 'My First blog!', content: 'my very first blog! :)', likes: 5, isPinned: false },
    { id: 2, user: 'user2', title: 'Hello Brother Band', content: 'This is awesome!', likes: 3, isPinned: true },
  ]

  const chats = [
    { id: 1, user: 'friend1', lastMessage: 'Hey, how are you?' },
    { id: 2, user: 'friend2', lastMessage: 'Did you see the new post?' },
  ]


  const logout = async () => {
    console.log(firebaseUser)
  }

  if (loading) return <Loading />

  return (
    <div className="min-h-screen bg-gray-100 font-mono text-black">
      <header className="bg-blue-500 text-white p-4 text-center">
        <h1 className="text-4xl font-bold animate-pulse">WeaveBond</h1>
      </header>

      <div className="container mx-auto p-4 flex flex-col md:flex-row gap-8">
        {/* Sidebar */}
        <aside className="md:w-1/3 space-y-4">
          <div className="bg-white p-4 border-2 border-black shadow-[4px_4px_0_0_rgba(0,0,0,1)]">
            <div className="flex flex-col items-center space-y-4">
              <div className="relative h-24 w-24 border-2 border-black">
                <img
                  src={user.profile_picture}
                  alt="Profile picture"
                  className="object-cover"
                />
              </div>
              <div className="text-center w-48">
                <h2 className="font-bold text-xl">{user.username}</h2>
                <div className="mt-2 space-y-1 flex flex-col items-start">
                  <p className='font-bold w-full flex justify-between'>- Friends <span>{user.friends.length}</span></p>
                  <p className='font-bold w-full flex justify-between'>- Likes <span>{user.friends.length}</span></p>
                  <p className='font-bold w-full flex justify-between'>- Posts <span>{user.friends.length}</span></p>
                </div>
              </div>
            </div>
          </div>
          <div className="space-y-2">
            {['WaveBond Cassette', 'Link Friend', 'Edit Profile', 'Logout'].map((text) => (
              <button
                key={text}
                className="cursor-pointer w-full bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 border-b-2 border-red-700 hover:border-red-800 active:border-t-2 active:border-b-0 transition-all duration-100"
              >
                {text}
              </button>
            ))}
          </div>
        </aside>

        {/* Main Content */}
        <main className="md:w-2/3">
          <div className="bg-white border-2 border-black p-4 shadow-[4px_4px_0_0_rgba(0,0,0,1)]">
            <div className="flex space-x-4 mb-4">
              <button
                onClick={() => setActiveTab('posts')}
                className={`flex-1 font-bold py-2 px-4 border-b-2 transition-all duration-100 ${
                  activeTab === 'posts' ? 'bg-blue-500 text-white border-blue-700' : 'bg-gray-200 border-gray-400'
                }`}
              >
                Posts
              </button>
              <button
                onClick={() => setActiveTab('inbox')}
                className={`flex-1 font-bold py-2 px-4 border-b-2 transition-all duration-100 ${
                  activeTab === 'inbox' ? 'bg-green-500 text-white border-green-700' : 'bg-gray-200 border-gray-400'
                }`}
              >
                Inbox
              </button>
              <button
                onClick={() => setActiveTab('my-posts')}
                className={`flex-1 font-bold py-2 px-4 border-b-2 transition-all duration-100 ${
                  activeTab === 'my-posts' ? 'bg-yellow-500 text-white border-yellow-700' : 'bg-gray-200 border-gray-400'
                }`}
              >
                My Posts
              </button>
            </div>

            {/* Search bar */}
            <div className="mb-4">
              <input
                type="text"
                placeholder="Search users and posts..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full px-3 py-2 border-2 border-black bg-gray-100"
              />
            </div>

            {activeTab === 'posts' && (
              <div className="space-y-4">
                {posts.map((post) => (
                  <div key={post.id} className="bg-gray-100 p-4 border-2 border-black">
                    <h3 className="font-bold">{post.title}</h3>
                    <p className="text-sm">{post.content}</p>
                    <p className="text-sm text-red-600 mt-2">♥ {post.likes} Likes</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'inbox' && (
              <div className="space-y-4">
                {chats.map((chat) => (
                  <div key={chat.id} className="bg-gray-100 p-4 border-2 border-black cursor-pointer hover:bg-gray-200">
                    <h3 className="font-bold">{chat.user}</h3>
                    <p className="text-sm">{chat.lastMessage}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'my-posts' && (
              <div className="space-y-4">
                {posts.map((post) => (
                  <div key={post.id} className="bg-gray-100 p-4 border-2 border-black">
                    <h3 className="font-bold">{post.title}</h3>
                    <p className="text-sm">{post.content}</p>
                    <p className="text-sm text-red-600 mt-2">♥ {post.likes} Likes</p>
                    <div className="mt-2 space-x-2">
                      <button className="bg-blue-500 text-white px-2 py-1 text-sm">
                        {post.isPinned ? 'Unpin' : 'Pin'}
                      </button>
                      <button className="bg-red-500 text-white px-2 py-1 text-sm">
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <button
            onClick={() => setIsModalOpen(true)}
            className="cursor-pointer fixed bottom-8 right-8 bg-pink-500 hover:bg-pink-600 text-white font-bold py-4 px-6 rounded-full border-2 border-black shadow-[4px_4px_0_0_rgba(0,0,0,1)] hover:shadow-[2px_2px_0_0_rgba(0,0,0,1)] active:shadow-none transition-all duration-100 animate-bounce"
          >
            Create Post
          </button>
        </main>
      </div>
      {/*
      <CreatePostModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
      */}
    </div>
  )
}

