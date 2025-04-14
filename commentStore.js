export class CommentStore {
    constructor() {
        this.comments = [];
    }

    setComments(comments) {
        this.comments = comments;
    }

    getComments() {
        return this.comments;
    }
}