import { UserProfileResponse } from '@line/bot-sdk/dist/messaging-api/api'
import { Injectable } from '@nestjs/common'
import { InjectModel } from '@nestjs/mongoose'
import { ReturnDocument } from 'mongodb'
import { Model } from 'mongoose'
import { LineMessage } from '../../db/entities/LineMessage'
import { LineUser } from '../../db/entities/LineUser'

@Injectable()
export class LineService {
  constructor(
    @InjectModel(LineUser.name) private lineUserModel: Model<LineUser>,
    @InjectModel(LineMessage.name) private lineMessageModel: Model<LineMessage>,
  ) {}

  async addLineUser(userProfile: UserProfileResponse) {
    const { userId, displayName } = userProfile
    const user = await this.lineUserModel.findOneAndUpdate(
      {
        userId,
      },
      {
        userId,
        name: displayName,
        isActive: true,
      },
      {
        upsert: true,
        returnDocument: ReturnDocument.AFTER,
      },
    )
    return user
  }

  async userUnFollow(userId: string) {
    const user = await this.lineUserModel.updateOne(
      {
        userId,
      },
      {
        isActive: false,
      },
    )
    return user
  }

  async addMessage(userId: string, message: string) {
    const lineMessage = await this.lineMessageModel.create({
      userId,
      message,
    })
    return lineMessage
  }

  async getMessageCanSend() {
    const usersActive = await this.lineUserModel.find({
      isActive: true,
    })
    const userIdsActive = usersActive.map((e) => e.userId)
    const lineMessages = await this.lineMessageModel.find({
      isSent: false,
      userId: userIdsActive,
    })
    return lineMessages
  }

  async markLineMessageSent(lineMessageIds: string[]) {
    if (!lineMessageIds.length) return []
    const lineMessages = await this.lineMessageModel.updateMany(
      {
        _id: { $in: lineMessageIds },
        isSent: false,
      },
      {
        $set: {
          isSent: true,
        },
      },
    )
    return lineMessages
  }
}
