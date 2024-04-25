const { prisma } = require('../prisma/prisma-client');

const FollowController = {
  followUser: async (req, res) => {
    const { followingId } = req.body;
    const userId = req.user.userId;
    if (followingId === userId) {
      return res
        .status(500)
        .json({ error: 'Не можете подписаться на самого себя' });
    }
    try {
      const existingSubsctiption = await prisma.follows.findFirst({
        where: { AND: [{ followerId: userId }, { followingId }] },
      });
      if (existingSubsctiption) {
        return res.status(400).json({ error: 'Вы уже подписаны' });
      }
      await prisma.follows.create({
        data: {
          follower: { connect: { id: userId } },
          following: { connect: { id: followingId } },
        },
      });
      res.status(201).json({ message: 'Подписка успешно создана' });
    } catch (error) {
      console.error('Error follow', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  },
  unfollowUser: async (req, res) => {
    const { followingId } = req.body;
    const userId = req.user.userId;
    try {
      const follows = await prisma.follows.findFirst({
        where: {
          AND: [
            {
              followerId: userId,
            },
            { followingId },
          ],
        },
      });
      if (!follows) {
        res
          .status(404)
          .json({ message: 'Вы не подписаны на этого пользователя' });
      }
      await prisma.follows.delete({
        where: { id: follows.id },
      });
      res.status(201).json({ message: 'Подписка успешно отменена' });
    } catch (error) {
      console.error('Error unfollow', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  },
};

module.exports = FollowController;
