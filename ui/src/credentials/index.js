let userCredentials = {
  administrator:{
    user: {
        create: true,
        modify: {all: true, self: true},
        delete: {all: true, self: false},
        list: {all: true, new: true, self: true},
    },
    educationalResources: {
        create: true,
        modify: {all: true, self: true},
        delete: {all: true, self: true},
        list: {
            all: true, new: true, reported: true, self: true,
            selfToEvaluate: false
        }
    },
    collections: {
        create: true,
        modify: true,
        delete: true,
        list: true,
    }
  },
  evaluator: {
    user: {
        create: false,
        modify: {all: false, self: true},
        delete: {all: false, self: true},
        list: {all: false, new: false, self: true},
    },
    educationalResources: {
        create: true,
        modify: {all: false, self: true},
        delete: {all: false, self: true},
        list: {
            all: true, new: false, reported: false, self: true,
            selfToEvaluate: true
        }
    }
  },
  creator: {
    user: {
        create: false,
        modify: {all: false, self: true},
        delete: {all: false, self: true},
        list: {all: false, new: false, self: true},
    },
    educationalResources: {
        create: true,
        modify: {all: false, self: true},
        delete: {all: false, self: true},
        list: {
            all: true, new: false, reported: false, self: true,
            selfToEvaluate: false
        }
    }
  },
  external: {
    user: {
        create: false,
        modify: {all: false, self: true},
        delete: {all: false, self: true},
        list: {all: false, new: false, self: true},
    },
    educationalResources: {
        create: false,
        modify: {all: false, self: false},
        delete: {all: false, self: false},
        list: {
            all: true, new: false, reported: false, self: false,
            selfToEvaluate: false
        }
    }
  }
};

export default userCredentials;
