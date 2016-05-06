# know-that-face
Field Session 2016: Facial recognition and query

## Index
* [The Team](#team)
* [Purpose](#purpose)
* [Suggested Techniques and Reading](#reading)

### <a name="team"></a>The Team
* You
  * Clayton Howeth 
    * <choweth@mines.edu> 
    * [@choweth](https://github.com/choweth)
  * Jed Menard 
    * <jmenard@mymail.mines.edu> 
    * [@jedmenard](https://github.com/jedmenard)
  * Patrick Nichols 
    * <panichol@mymail.mines.edu> 
    * [@panichol](https://github.com/panichol)
* Us
  * Jack Kelly 
    * <jack@fullcontact.com> 
    * [@johkelly](https://github.com/johkelly)
    * Mines 2014 alum, Field Session 2013. Technical lead.
  * Ken Michie 
    * <ken@fullcontact.com> 
    * [@mcmancsu](https://github.com/mcmancsu)
    * Senior Software Engineer at FullContact. Managerial lead.

### <a name="purpose"></a>Purpose
FullContact has a lot of images from social profiles, on the order of billions. A significant portion of these are out of date, low quality, not visually representative, duplicates, etc.; however, a non-trivial portion of them are good images of the associated person's face:

![Travis Todd, our CTO](https://d2ojpxxtu63wzl.cloudfront.net/static/97a0bc471cc3a26414480bad5d6bb070_7bb1bf3436444627ab209d7159ec5c4d150bddc3b109285efd090e77806c07f3)

What we would like is some way to query using a new image: 

![Travis Todd, again](https://marketing-cdn1.fullcontact.com/wp-content/uploads/2015/12/travis.jpg)

And retrieve the FullContact Person API profile that the original image(s) for the person are attached to:

```json

  "status": 200,
  "requestId": "c3f7a254-b2d2-4d27-a945-f121603f6f9d",
  "likelihood": 0.87,
  "photos": [
    {
      "type": "facebook",
      "typeId": "facebook",
      "typeName": "Facebook",
      "url": "https://d2ojpxxtu63wzl.cloudfront.net/static/3ac3cd006f1a467719c8df5b44626984_62537b0dd32e98dbf41ba419ed33c1968d69a1ae31a57ffe274dab6ea1ca6e89",
      "isPrimary": true
    },
    {
      "type": "linkedin",
      "typeId": "linkedin",
      "typeName": "LinkedIn",
      "url": "https://d2ojpxxtu63wzl.cloudfront.net/static/97a0bc471cc3a26414480bad5d6bb070_7bb1bf3436444627ab209d7159ec5c4d150bddc3b109285efd090e77806c07f3",
      "isPrimary": false
    },
    {
      "type": "google",
      "typeId": "google",
      "typeName": "GooglePlus",
      "url": "https://d2ojpxxtu63wzl.cloudfront.net/static/d4fbece0d42660711d8320cd24ed6ebe_7c04c0cc814a31af22f72aac2da772abab2d6b8970bdb453d01c0d1e4a16152d",
      "isPrimary": false
    },
    {
      "type": "gravatar",
      "typeId": "gravatar",
      "typeName": "Gravatar",
      "url": "https://d2ojpxxtu63wzl.cloudfront.net/static/58cd0a85261c5da33162a32da488dda0_6d078ccac1e2e46c90d73304e40b6ac9c9a1a3c6e12007a1bf0fd6fb638322f6",
      "isPrimary": false
    },
    {
      "type": "googleplus",
      "typeId": "googleplus",
      "typeName": "GooglePlus",
      "url": "https://d2ojpxxtu63wzl.cloudfront.net/static/d4fbece0d42660711d8320cd24ed6ebe_7c04c0cc814a31af22f72aac2da772abab2d6b8970bdb453d01c0d1e4a16152d",
      "isPrimary": false
    }
  ],
  "contactInfo": {
    "websites": [
      {
        "url": "http://travi.st"
      }
    ],
    "familyName": "Todd",
    "fullName": "Travis Todd",
    "givenName": "Travis"
  },
  "etc": "..."
}
```

For the purposes of this field session we think it will be acceptable to accomplish this search functionality within the scope of the employees at FullContact's Denver office. If the project moves quickly, or the chosen technique shows great promise, it would be great to expand this scope to an arbitrary subset of the profiles maintained by FullContact.

We have some ideas for how this can be implemented (see the next section). However, there is room for using different techniques or technologies if you believe they will be more effective. Feel free to investigate and experiment, but be aware that our time together on this project is limited!

### <a name="reading"></a>Suggested Techniques and Reading

Solving this problem satisfactorily will involve multiple layers of technology and algorithms. We've prepared several reading items that may be worth your time to become familiar with before we begin the project. And if you've already seen/read some of these before -- great! This is by no means an exhaustive list of what will be relevant for solving the problem at hand, merely a sampling of readings which might be useful.

#### Eigenfaces/Fisherfaces
A key component of this project will be finding a way to describe faces such that they can be matched quickly and reliably at query-time. Two potential approaches are Eigenfaces and Fisherfaces. These techniques treat images of faces as high-dimensional vectors, and leverage PCA and LDA to describe the "faces" in the corresponding high-dimensional space which represent the most distinctive visual components of the faces. I'm taking significant liberties with that summary, so you may want to read up on the underlying techniques so we discuss them together:

* [PCA](https://en.wikipedia.org/wiki/Principal_component_analysis): Principal Component Analysis
* [LDA](https://en.wikipedia.org/wiki/Linear_discriminant_analysis): Linear Discriminant Analysis
* [EigenFaces](https://en.wikipedia.org/wiki/Eigenface)
* [FisherFaces](http://docs.opencv.org/2.4/modules/contrib/doc/facerec/facerec_tutorial.html#fisherfaces)

#### OpenCV
A _de facto_ standard for image processing and manipulation. Has bindings for nearly any language imaginable because its uses a C interface. [The docs](http://docs.opencv.org/2.4/modules/refman.html) are large, but you can you skim the [User Guide](http://docs.opencv.org/2.4/doc/user_guide/user_guide.html) and [Tutorials](http://docs.opencv.org/2.4/doc/tutorials/tutorials.html) to get an idea for the sorts of things you can do with OpenCV.

#### ElasticSearch
Fuzzy search at scale. There's a lot of power here -- don't wory if you can't grok it all. We think ES has the potential to handle the reverse-face-search problem at scale with clever indexing.

* [Wikipedia article](https://en.wikipedia.org/wiki/Elasticsearch)
* [GitHub Repo](https://github.com/elastic/elasticsearch): Includes a tutorial!
* [image-match](https://github.com/ascribe/image-match): An interesting project doing something similar. Their search algorithm might be very interesting for this project.
