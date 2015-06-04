# This example demonstrates options to export and import topic model.
import glob
import uuid

import artm.messages_pb2
import artm.library

# Load one test batch
batches_disk_path = 'kos'
batches = glob.glob(batches_disk_path + "/*.batch")
test_batch = artm.library.Library().LoadBatch(batches[0])

with artm.library.MasterComponent() as master:
    model = master.CreateModel(topics_count=10)
    for iteration in range(0, 2):
        master.InvokeIteration(disk_path=batches_disk_path)
        master.WaitIdle()
        model.Synchronize()
    filename = str(uuid.uuid1())

    # Export topic model into file in binary format
    model.Export(filename)

    theta_matrix = master.GetThetaMatrix(model=model, batch=test_batch)
    print "Theta distribution for one test document: "
    print "For the original topic model:             ",
    for value in theta_matrix.item_weights[0].value:
        print "%.5f" % value,

with artm.library.MasterComponent() as master2:
    model = master2.CreateModel(topics_count=10)

    # Import topic model from binary file
    model.Import(filename)

    theta_matrix = master2.GetThetaMatrix(model=model, batch=test_batch)
    print "\nFor topic model imported into test_master:",
    for value in theta_matrix.item_weights[0].value:
        print "%.5f" % value,