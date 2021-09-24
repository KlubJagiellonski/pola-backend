import { Friend } from '../../domain/friends';

export function getRandomFriend(friends: Friend[]) {
  const randomNumber = Math.floor(Math.random() * friends.length);
  return friends[randomNumber];
}

export function getFriendBySlug(slug: string, friends: Friend[]) {
  return friends.find((friend) => friend.slug === slug);
}
