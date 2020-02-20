from zlib import crc32
ENDSIG = 0x06054B50

def sizeof(format):
	return sum(format[0].values())

file_entry = ({
	"signature": 4,
	"min_version": 2,
	"general_flag": 2,
	"compression": 2,
	"lastmod_time": 2,
	"lastmod_date": 2,
	"crc32": 4,
	"csize": 4,
	"usize": 4,
	"filename_size": 2,
	"extra_size": 2,
}, {
	"filename": "filename_size",
	"extra": "extra_size",
	"data": "csize",
})

cdir_entry = ({
	"signature": 4,
	"creator_version": 2,
	"min_version": 2,
	"general_flag": 2,
	"compression": 2,
	"lastmod_time": 2,
	"lastmod_date": 2,
	"crc32": 4,
	"csize": 4,
	"usize": 4,
	"filename_size": 2,
	"extra_size": 2,

	"comment_size": 2,
	"disknum": 2,
	"internal_attr": 2,
	"external_attr": 4,
	"offset": 4,
}, {
	"filename": "filename_size",
	"extra": "extra_size",
	"comment": "comment_size",
})

cdir_end = ({
	"signature": 4,
	"disk_num": 2,
	"cdir_disk": 2,
	"disk_entries": 2,
	"cdir_entries": 2,
	"cdir_size": 4,
	"cdir_offset": 4,
	"comment_size": 2,
}, {
	"comment": "comment_size",
})

class MyStruct(dict):
	def __init__(self, format):
		self.format = format

	def pack(self):
		values = []
		for name in self.format[0]: values.append(self[name])
		extra_data = bytearray()
		for name in self.format[1]: extra_data += self[name]
		return b"".join(int.to_bytes(self[k], v, "little") for k, v in self.format[0].items()) \
			+ b"".join(self[k] for k in self.format[1])

class BinaryBlob:
	def __init__(self, f):
		self.data = open(f, "rb").read()
		self.offset = 0
		self.length = len(self.data)

	def readAt(self, pos, length):
		self.offset = pos + length
		return self.data[pos:pos+length]

	def read_struct(self, format, offset):
		self.offset = offset
		ret = MyStruct(format)
		for k, v in format[0].items(): ret[k] = int.from_bytes(self.readAt(self.offset, v), "little")
		for k, v in format[1].items(): ret[k] =                self.readAt(self.offset, ret[v])
		assert ret.pack() == self.readAt(offset, self.offset - offset)
		return ret

def optimizejar(jar, outjar, f):
	jarblob = BinaryBlob(jar)
	dirend = jarblob.read_struct(cdir_end, jarblob.length - sizeof(cdir_end))
	assert dirend["signature"] == ENDSIG

	jarblob.offset = dirend["cdir_offset"]
	cdir = [jarblob.read_struct(cdir_entry, jarblob.offset) for _ in range(dirend["cdir_entries"])]

	readahead = int.from_bytes(jarblob.readAt(0, 4), "little")
	[nreadahead] = [ i for i, f in enumerate(cdir) if f["offset"] == readahead ]

	with open(outjar, "wb") as fd:
		cdir_data = bytearray()

		fd.seek(4 + dirend["cdir_size"] + sizeof(cdir_end))
		for i, info in enumerate(cdir):
			if i == nreadahead:
				readahead = fd.tell()

			file = jarblob.read_struct(file_entry, info["offset"])
			assert file["filename"] == info["filename"]
			assert info["csize"] == info["usize"] == file["csize"] == file["usize"]

			info["offset"] = file["offset"] = fd.tell()
			file["data"] = f(file["filename"], file["data"])
			file["csize"] = file["usize"] = info["csize"] = info["usize"] = len(file["data"])
			file["crc32"] = info["crc32"] = crc32(file["data"])

			cdir_data += info.pack()
			fd.write(file.pack())

		dirend["cdir_offset"] = 4
		dirend["cdir_size"] = len(cdir_data)
		dirend["disk_entries"] = dirend["cdir_entries"]
		dirend_data = dirend.pack()
		fd.write(dirend_data)

		fd.seek(dirend["cdir_offset"])
		fd.write(cdir_data)
		fd.write(dirend_data)

		fd.seek(0)
		fd.write(int.to_bytes(readahead, 4, "little"))
