from zlib import crc32

def sizeof(format):
	return sum(format[0].values())

file_entry = ({
	"file_signature": 4,
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
	"cdir_signature": 4,
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
	"end_signature": 4,
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

def pack(format, self):
	return (
		b"".join(int.to_bytes(self[k], v, "little") for k, v in format[0].items())
		+ b"".join(self[k] for k in format[1])
	)

class BinaryBlob:
	def __init__(self, f):
		self.data = f.read()
		self.offset = 0
		self.length = len(self.data)

	def readAt(self, pos, length):
		self.offset = pos + length
		return self.data[pos:pos+length]

	def read_struct(self, format, offset):
		self.offset = offset
		ret = {}
		for k, v in format[0].items(): ret[k] = int.from_bytes(self.readAt(self.offset, v), "little")
		for k, v in format[1].items(): ret[k] =                self.readAt(self.offset, ret[v])
		assert pack(format, ret) == self.readAt(offset, self.offset - offset)
		return ret

def entry(name, data, *, offset, prio=False, permissions=0):
	return {
		"cdir_signature": 0x02014B50,
		"file_signature": 0x04034B50,

		"min_version": 10,
		"creator_version": 0x0314 if permissions else 0x0014,
		"general_flag": 0,
		"compression": 0,
		"lastmod_time": 0,
		"lastmod_date": 15393,

		"disknum": 0,
		"internal_attr": 0,
		"external_attr": permissions,

		"extra_size": 0,
		"extra": b"",

		"comment_size": 0,
		"comment": b"",

		"offset": offset,

		"filename_size": len(name),
		"filename": name,

		"crc32": crc32(data),
		"csize": len(data),
		"usize": len(data),
		"data": data,
	}

def read(fd):
	jarblob = BinaryBlob(fd)
	dirend = jarblob.read_struct(cdir_end, jarblob.length - sizeof(cdir_end))
	assert dirend["end_signature"] == 0x06054B50

	jarblob.offset = dirend["cdir_offset"]
	cdir = [jarblob.read_struct(cdir_entry, jarblob.offset) for _ in range(dirend["cdir_entries"])]

	readahead = int.from_bytes(jarblob.readAt(0, 4), "little")

	files = {}
	for i, info in enumerate(cdir):
		file = jarblob.read_struct(file_entry, info["offset"])
		name = file["filename"]
		data = file["data"]
		files[name.decode()] = spec = {
			"prio": jarblob.offset <= readahead,
			"permissions": info["external_attr"],
			"data": data,
		}

		ent = entry(**spec, name=name, offset=info["offset"])
		for k in info: assert info[k] == ent.get(k), (k, info[k], ent.get(k))
		for k in file: assert file[k] == ent.get(k), (k, file[k], ent.get(k))
	return files

def write(fd, files):
	files = [(k.encode(), v) for k, v in files.items()]

	cdir = bytearray()
	body = bytearray()
	cdir_size = sum(sizeof(cdir_entry) + len(n) for (n, f) in files)
	offset = 4+sizeof(cdir_end)+cdir_size
	for n, f in files:
		if f["prio"]:
			ent = entry(**f, name=n, offset=offset+len(body))
			cdir.extend(pack(cdir_entry, ent))
			body.extend(pack(file_entry, ent))
	readahead = offset+len(body)
	for n, f in files:
		if not f["prio"]:
			ent = entry(**f, name=n, offset=offset+len(body))
			cdir.extend(pack(cdir_entry, ent))
			body.extend(pack(file_entry, ent))

	assert len(cdir) == cdir_size

	end = {
		"end_signature": 0x06054B50,
		"disk_num": 0,
		"cdir_disk": 0,
		"disk_entries": len(files),
		"cdir_entries": len(files),
		"cdir_size": cdir_size,
		"cdir_offset": 4,
		"comment_size": 0,
		"comment": b""
	}

	fd.write(int.to_bytes(readahead, 4, "little"))
	fd.write(cdir)
	fd.write(pack(cdir_end, end))
	fd.write(body)
	fd.write(pack(cdir_end, end))
